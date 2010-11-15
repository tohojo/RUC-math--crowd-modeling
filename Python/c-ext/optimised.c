#include "optimised.h"

static double A_1, A_2, B_1, B_2, timestep;
static Py_ssize_t use_threads;

// Global objects to allow access from different threads
static PyObject ** p_actors;
static Actor * actors;
static Wall * walls;
static Py_ssize_t a_count;
static Py_ssize_t w_count;

// Threading variables
static pthread_mutex_t start_mutex;
static pthread_cond_t start_cond;
static pthread_t * threads;
static pthread_attr_t thread_attr;

static PyObject * update_actors(PyObject * self, PyObject * args)
{
    // Python objects
    PyObject * p_actor_list; // List of other actors
    PyObject * p_walls; // List of walls


    int i,j = 0;

    PyArg_ParseTuple(args, "OO:update_actors", &p_actor_list, &p_walls);


    a_count = PyList_Size(p_actor_list);
    w_count = PyList_Size(p_walls);

    actors   = PyMem_Malloc(a_count * sizeof(Actor));
    walls    = PyMem_Malloc(w_count * sizeof(Wall));
    p_actors = PyMem_Malloc(a_count * sizeof(PyObject*));

    for(i = 0; i < a_count; i++) {
        PyObject * p_a = PyList_GetItem(p_actor_list, i);
        actor_from_pyobject(p_a, &actors[i]);
        p_actors[i] = p_a;

        actors[i].acceleration.x = 0.0;
        actors[i].acceleration.y = 0.0;
    }

    // Since we are not touching any python objects in this part, 
    // we can release the global interpreter lock, to allow for multithreaded
    // goodness.
    Py_BEGIN_ALLOW_THREADS

        do_calculations();

    Py_END_ALLOW_THREADS

    for(i = 0; i < a_count; i++) {
        update_python_objects(actors, p_actors, a_count);
    }

    PyMem_Free(walls);
    PyMem_Free(actors);
    PyMem_Free(p_actors);


    Py_RETURN_NONE;
}

static void do_calculations()
{
    int i, rc;
    void * status;
    if(use_threads) {
        Part * parts;
        parts = PyMem_Malloc(use_threads * sizeof(Part));
        int part_len = a_count / use_threads;
        for(i = 0; i < use_threads; i++) {
            parts[i].start = i*part_len;
            parts[i].end = (i+1)*part_len;
        }
        parts[use_threads-1].end += a_count % use_threads;

        for(i = 0; i < use_threads; i++) {
            rc = pthread_create(&threads[i], NULL, 
                    do_calculation_part, (void *) &parts[i]);
        }

        for(i = 0; i < use_threads; i++) {
            pthread_join(threads[i], &status);
        }
    } else {
        Part p = {0, a_count};
        do_calculation_part(&p);
    }

    for(i = 0; i < a_count; i++) {
        update_position(&actors[i]);
    }
}

static void do_calculation_part(Part * p)
{
    int i,j;
    for(i = p->start; i < p->end; i++) {
        add_desired_acceleration(&actors[i]);

        for(j = 0; j < a_count; j++) {
            if(i == j) continue;
            add_repulsion(&actors[i], &actors[j]);
        }
    }
    if(use_threads) pthread_exit(NULL);
}

static void add_desired_acceleration(Actor * a)
{
    /* Equivalent Python code:
     
        # To compute the impatience factor, we need the average velocity,
        # in the direction of desired movement.
        #
        # This is found by projecting the direction we have moved onto the
        # vector from the initial position to the target and computing the
        # distance from this projection. The distance travelled is then
        # converted to an average velocity my dividing with the time
        if self.time == 0.0:
            average_velocity = 0.0
        else:
            proj = Vector.projection_length(
                       self.initial_position, self.target, self.position)


            average_velocity = proj / self.time

        # The impatience factor is given by the average velocity divided
        # by the *initial* desired velocity. (6) in the article
        impatience = 1.0 - average_velocity / self.initial_desired_velocity

        # (5) in the article
        desired_velocity = (1.0-impatience) * self.initial_desired_velocity + \
                impatience * self.max_velocity

        towards_target = (self.target - self.position).normal()

        #desired_acceleration = (1.0/self.relax_time) * \
                #(desired_velocity * towards_target - self.velocity)
        towards_target *= desired_velocity
        towards_target -= self.velocity
        towards_target *= (1.0/self.relax_time)

        self.acceleration = towards_target
        */

    double average_velocity, impatience, desired_velocity = 0.0;
    Vector towards_target = {0.0, 0.0};

    if(a->time) {
        double proj = vector_projection_length(
                a->initial_position, a->target, a->position);
        average_velocity = proj / a->time;
    }

    impatience = 1.0 - average_velocity / a->initial_desired_velocity;

    desired_velocity = (1.0-impatience) * a->initial_desired_velocity + \
                       impatience * a->max_velocity;
    towards_target = vector_sub(a->target, a->position);
    vector_normalise(&towards_target);


    vector_imul(&towards_target, desired_velocity);
    vector_isub(&towards_target, &a->velocity);
    vector_imul(&towards_target, 1.0/a->relax_time);

    a->acceleration = towards_target;

}

void add_repulsion(Actor * a, Actor * b)
{
    /* Equivalent Python code:
     
            radius_sum = b.radius + self.radius

            from_b = self.position - b.position
            distance = from_b.length()

            from_b.normalize(distance)
            from_b *= pm.constants.a_2 * \
                    numpy.exp((radius_sum-distance)/pm.constants.b_2)

    */

    double radius_sum = a->radius + b->radius;
    Vector from_b     = vector_sub(a->position, b->position);
    double distance   = vector_length(from_b);
    //if(isnan(distance)) return;

    vector_normalise(&from_b);
    vector_imul(&from_b, A_2 * exp((radius_sum-distance)/B_2));

    vector_iadd(&a->acceleration, &from_b);
}

void update_position(Actor * a)
{
    /* Equivalent Python code:
        # Calculate displacement from acceleration and velocity
        delta_p = Vector(
                self.velocity.x * timestep + 0.5 * self.acceleration.x * timestep**2,
                self.velocity.y * timestep + 0.5 * self.acceleration.y * timestep**2)

        # Update position and velocity, and reset the acceleration
        self.position += delta_p
        self.velocity += self.acceleration
        self.time += timestep
    */

    Vector delta_p;

    delta_p.x = a->velocity.x * timestep + 0.5 * a->acceleration.x * pow(timestep, 2);
    delta_p.y = a->velocity.y * timestep + 0.5 * a->acceleration.y * pow(timestep, 2);


    vector_iadd(&a->position, &delta_p);
    vector_iadd(&a->velocity, &a->acceleration);
    a->time += timestep;
}

void update_python_objects(Actor * actors, PyObject ** p_actors, Py_ssize_t n)
{
    int i;
    for(i = 0; i < n; i++) {
        PyObject * update_p_res;
        PyObject * update_v_res;
        PyObject * update_t_res;

        update_p_res = PyObject_CallMethod(p_actors[i], "set_position", "dd",
                actors[i].position.x, actors[i].position.y);
        update_v_res = PyObject_CallMethod(p_actors[i], "set_velocity", "dd",
                actors[i].velocity.x, actors[i].velocity.y);
        update_t_res = PyObject_CallMethod(p_actors[i], "set_time", "(d)",
                actors[i].time);

        Py_DECREF(update_p_res);
        Py_DECREF(update_v_res);
        Py_DECREF(update_t_res);
    }
}

static Actor actor_from_pyobject(PyObject * o, Actor * a)
{
    a->radius                   = double_from_attribute(o, "radius");
    a->time                     = double_from_attribute(o, "time");
    a->initial_desired_velocity = double_from_attribute(o, "initial_desired_velocity");
    a->max_velocity             = double_from_attribute(o, "max_velocity");
    a->relax_time               = double_from_attribute(o, "relax_time");


    a->position         = vector_from_attribute(o, "position");
    a->initial_position = vector_from_attribute(o, "initial_position");
    a->target           = vector_from_attribute(o, "target");
    a->velocity         = vector_from_attribute(o, "velocity");
}

static Py_ssize_t ssize_t_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyObject_GetAttrString(o, name);
    Py_ssize_t result = PyInt_AsSsize_t(o2);
    Py_DECREF(o2);
    return result;
}

static double double_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyObject_GetAttrString(o, name);
    double result = PyFloat_AsDouble(o2);
    Py_DECREF(o2);
    return result;
}

static Vector vector_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyObject_GetAttrString(o, name);
    Vector result = vector_from_pyobject(o2);
    Py_DECREF(o2);
    return result;
}

static Vector vector_from_pyobject(PyObject * o)
{
    Vector v;

    PyObject * x = PyObject_GetAttrString(o, "x");
    PyObject * y = PyObject_GetAttrString(o, "y");
    v.x = PyFloat_AsDouble(x);
    v.y = PyFloat_AsDouble(y);

    Py_DECREF(x);
    Py_DECREF(y);

    return v;
}

static PyMethodDef OptimisedMethods[] = {
    {"update_actors", update_actors, METH_VARARGS, 
        "Calculate the acceleration of an actor"},
};

PyMODINIT_FUNC initoptimised(void)
{
    PyObject * p_module;
    PyObject * p_constants;

    (void) Py_InitModule("optimised", OptimisedMethods);
    Py_AtExit(cleanup);

    p_module    = PyImport_ImportModule("parameters");
    p_constants = PyObject_GetAttrString(p_module, "constants");
    A_2         = double_from_attribute(p_constants, "a_2");
    B_2         = double_from_attribute(p_constants, "b_2");
    timestep    = double_from_attribute(p_module, "timestep");
    use_threads = ssize_t_from_attribute(p_module, "use_threads");
    Py_DECREF(p_module);
    Py_DECREF(p_constants);

    if(use_threads) init_threads();
}

static void cleanup()
{
    if(use_threads) destroy_threads();
}

static void init_threads()
{
    threads = PyMem_Malloc(use_threads * sizeof(pthread_t));
    //pthread_mutex_init(&start_mutex, NULL);
    //pthread_cond_init(&start_cond, NULL);

    pthread_attr_init(&thread_attr);
    pthread_attr_setdetachstate(&thread_attr, PTHREAD_CREATE_JOINABLE);

}

static void destroy_threads()
{
    pthread_attr_destroy(&thread_attr);
    //pthread_mutex_destroy(&start_mutex);
    //pthread_cond_destroy(&start_cond);
    PyMem_Free(threads);
}
