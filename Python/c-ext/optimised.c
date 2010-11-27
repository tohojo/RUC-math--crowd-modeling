#include "optimised.h"

/*** Calculation part begin ***/

static double A_1, A_2, B_1, B_2, U, timestep;

// Global objects to allow access from different threads
static Actor * actors;
static Wall * walls;
static Py_ssize_t a_count;
static Py_ssize_t w_count;

void calculate_forces(Py_ssize_t i)
{
    int j;
    add_desired_acceleration(&actors[i]);

    for(j = 0; j < a_count; j++) {
        if(i == j) continue;
        add_repulsion(&actors[i], &actors[j]);
    }

    add_wall_repulsion(&actors[i]);
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

void add_wall_repulsion(Actor * a)
{
    int i;
    Vector * repulsion_points  = PyMem_Malloc(w_count * sizeof(Vector));
    int rep_p_c = 0;
    Vector repulsion;

    rep_p_c = find_repultion_points(a, repulsion_points);

    for(i = 0; i < rep_p_c; i++) {
        repulsion = calculate_wall_repulsion(a, repulsion_points[i]);
        //printf("(%f,%f)\n", repulsion.x, repulsion.y);
        vector_iadd(&a->acceleration, &repulsion);
    }


    PyMem_Free(repulsion_points);
}

int find_repultion_points(Actor * a, Vector repulsion_points[])
{
    int i,j;
    double projection_length;
    Vector * used_endpoints    = PyMem_Malloc(2*w_count * sizeof(Vector));
    Vector * possible_endpoints = PyMem_Malloc(w_count * sizeof(Vector));
    int rep_p_c = 0, use_e_c = 0, pos_e_c = 0;

    for(i = 0; i < w_count; i++) {
        Wall w = walls[i];
        projection_length = vector_projection_length(w.start, w.end, a->position);
        if(projection_length < 0)  {
            possible_endpoints[pos_e_c++] = w.start;
        } else if(projection_length > w.length) {
            possible_endpoints[pos_e_c++] = w.end;
        } else {
            // We have the length, L, of how far along AB the projection point is.
            // To turn this into a point, we multiply AB with L/|AB| and add
            // this vector to the starting point A.
            repulsion_points[rep_p_c++] = vector_add(w.start, 
                    vector_mul(vector_sub(w.end, w.start), 
                        projection_length/w.length));
            used_endpoints[use_e_c++] = w.start;
            used_endpoints[use_e_c++] = w.end;
        }
    }

    for(i = 0; i < pos_e_c; i++) {
        int use_e = 1;
        for(j = 0; j < use_e_c; j++) {
            if(possible_endpoints[i].x == used_endpoints[j].x && 
                    possible_endpoints[i].y == used_endpoints[j].y) {
                use_e = 0;
            }
        }
        if(use_e) {
            repulsion_points[rep_p_c++] = possible_endpoints[i];
            used_endpoints[use_e_c++] = possible_endpoints[i];
        }
    }

    PyMem_Free(used_endpoints);
    PyMem_Free(possible_endpoints);

    return rep_p_c;
}

Vector calculate_wall_repulsion(Actor * a, Vector repulsion_point)
{
    Vector repulsion = {0,0};
    Vector repulsion_vector = vector_sub(repulsion_point, a->position);
    double repulsion_length = vector_length(repulsion_vector);

    repulsion.x = U * (1/a->radius) * \
                  (exp(-repulsion_length/a->radius)*\
                   (a->position.x-repulsion_point.x))/repulsion_length;
    repulsion.y = U * (1/a->radius) * \
                  (exp(-repulsion_length/a->radius)*\
                   (a->position.y-repulsion_point.y))/repulsion_length;

    return repulsion;
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

static int is_escaped(Actor * a)
{
	double l = vector_length(vector_sub(a->target, a->position));
	return (l <= a->radius*2);
}


/*** Calculation part end ***/



// Threading variables
static Py_ssize_t use_threads;
static pthread_t * threads;
static pthread_attr_t thread_attr;

static PyObject * update_actors(PyObject * self, PyObject * args)
{

    // Since we are not touching any python objects in this part, 
    // we can release the global interpreter lock, to allow for multithreaded
    // goodness.
    Py_BEGIN_ALLOW_THREADS

        do_calculations();

    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

static PyObject * add_actors(PyObject * self, PyObject * args)
{
    PyObject * p_actor_list;
    int i;

    PyArg_ParseTuple(args, "O:add_actors", &p_actor_list);
    a_count = PyList_Size(p_actor_list);
    actors   = PyMem_Realloc(actors, a_count * sizeof(Actor));

    for(i = 0; i < a_count; i++) {
        PyObject * p_a = PyList_GetItem(p_actor_list, i);
        actor_from_pyobject(p_a, &actors[i]);
    }
    Py_RETURN_NONE;
}

static PyObject * get_actor(PyObject * self, PyObject * args)
{
    Py_ssize_t i;

    PyArg_ParseTuple(args, "i:get_actor", &i);

	if(i > a_count) Py_RETURN_NONE;

    return Py_BuildValue("ddd", 
            actors[i].position.x, actors[i].position.y, actors[i].radius);
}

static PyObject * get_actors(PyObject * self, PyObject * args)
{
	PyObject * list = PyList_New(a_count);
	int i;

	for(i = 0; i < a_count; i++) {
		PyList_SetItem(list, i, Py_BuildValue("ddd", 
            actors[i].position.x, actors[i].position.y, actors[i].radius));
	}

    return list;
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

	check_escapes();
}

static void do_calculation_part(Part * p)
{
    int i,j;
    for(i = p->start; i < p->end; i++) {
        calculate_forces(i);
    }
    if(use_threads) pthread_exit(NULL);
}

static void check_escapes()
{
	int i, j;

	for(i = 0, j = 0; i < a_count; i++) {
		if(!is_escaped(&actors[i])) {
			actors[j++] = actors[i];
		}
	}

    if(i != j) {
        a_count -= i-j;
        actors = PyMem_Realloc(actors, a_count * sizeof(Actor));
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
    a->acceleration     = vector_from_attribute(o, "acceleration");
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
    {"add_actors", add_actors, METH_VARARGS, 
        "Add actors to the list"},
    {"get_actor", get_actor, METH_VARARGS, 
        "Get an actor's position and radius"},
    {"get_actors", get_actors, METH_VARARGS, 
        "Get all actor's position and radius"},
};

PyMODINIT_FUNC initoptimised(void)
{
    PyObject * p_module;
    PyObject * p_constants;
    PyObject * p_actors;
    PyObject * p_walls;

    (void) Py_InitModule("optimised", OptimisedMethods);
    Py_AtExit(cleanup);

    p_module    = PyImport_ImportModule("parameters");
    p_constants = PyObject_GetAttrString(p_module, "constants");
    p_actors    = PyObject_GetAttrString(p_module, "actor");
    p_walls     = PyObject_GetAttrString(p_module, "walls");
    A_2         = double_from_attribute(p_constants, "a_2");
    B_2         = double_from_attribute(p_constants, "b_2");
    U           = double_from_attribute(p_constants, "u");
    timestep    = double_from_attribute(p_module, "timestep");
    use_threads = ssize_t_from_attribute(p_module, "use_threads");
    a_count     = 0;
    actors      = NULL;

    init_walls(p_walls);

    Py_DECREF(p_module);
    Py_DECREF(p_constants);
    Py_DECREF(p_actors);
    Py_DECREF(p_walls);

    if(use_threads) init_threads();
}

static void init_walls(PyObject * p_walls)
{
    int i;
    w_count = PyList_Size(p_walls);
    walls    = PyMem_Malloc(w_count * sizeof(Wall));
    for(i = 0; i < w_count; i++) {
        PyObject * p_w   = PyList_GetItem(p_walls, i);
        walls[i].start.x = PyFloat_AsDouble(PyTuple_GetItem(p_w, 0));
        walls[i].start.y = PyFloat_AsDouble(PyTuple_GetItem(p_w, 1));
        walls[i].end.x   = PyFloat_AsDouble(PyTuple_GetItem(p_w, 2));
        walls[i].end.y   = PyFloat_AsDouble(PyTuple_GetItem(p_w, 3));
        walls[i].length  = vector_length(vector_sub(walls[i].end, walls[i].start));
    }
}

static void cleanup()
{
    if(use_threads) destroy_threads();
}

static void init_threads()
{
    threads = PyMem_Malloc(use_threads * sizeof(pthread_t));
    pthread_attr_init(&thread_attr);
    pthread_attr_setdetachstate(&thread_attr, PTHREAD_CREATE_JOINABLE);

}

static void destroy_threads()
{
    pthread_attr_destroy(&thread_attr);
    PyMem_Free(threads);
}
