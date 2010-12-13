#include "optimised.h"

/*** Calculation part begin ***/

static double A, B, U, lambda, timestep;

static Vector flowline[2];

// Global objects to allow access from different threads
static Pedestrian * pedestrians;
static Wall * walls;
static Py_ssize_t a_count;
static Py_ssize_t w_count;

static PyObject * module_dict;

void calculate_forces(Py_ssize_t i)
{
    int j;
    add_desired_acceleration(&pedestrians[i]);

    for(j = 0; j < a_count; j++) {
        if(i == j) continue;
        add_repulsion(&pedestrians[i], &pedestrians[j]);
    }

    add_wall_repulsion(&pedestrians[i]);
}

static void add_desired_acceleration(Pedestrian * a)
{
    double average_velocity = 0.0, impatience = 0.0, 
		   desired_velocity = 0.0;
    Vector desired_direction = {0.0, 0.0};

    if(a->time) {
        double proj = vector_projection_length(
                a->initial_position, a->target, a->position);
        average_velocity = proj / a->time;

		impatience = 1.0 - average_velocity / a->initial_desired_velocity;

		desired_velocity = (1.0-impatience) * a->initial_desired_velocity + \
						   impatience * a->max_velocity;

    } else {
		desired_velocity = a->initial_desired_velocity;
	}
    desired_direction = vector_sub(a->target, a->position);
    vector_unitise(&desired_direction);

	a->acceleration = vector_mul(desired_direction, desired_velocity);
    vector_isub(&a->acceleration, &a->velocity);
    vector_imul(&a->acceleration, 1.0/a->relax_time);

}

Vector calculate_repulsion(Pedestrian * a, Pedestrian * b, double A, double B)
{
    double radius_sum = a->radius + b->radius;
    Vector from_b     = vector_sub(a->position, b->position);
    double distance   = vector_length(from_b);

    vector_unitise(&from_b);
    vector_imul(&from_b, A * exp((radius_sum-distance)/B));

    return from_b;
}

void add_repulsion(Pedestrian * a, Pedestrian * b)
{
    if(!A || !B) return;
    Vector repulsion = calculate_repulsion(a, b, A, B);
	if(a->velocity.x && a->velocity.y && lambda < 1.0) {
		Vector from_b = vector_sub(b->position, a->position);

		double cosine = vector_dot(a->velocity, from_b)/(
				vector_length(a->velocity) * vector_length(from_b));

		vector_imul(&repulsion, (lambda + (1-lambda)*((1+cosine)/2)));
	}
    vector_iadd(&a->acceleration, &repulsion);
}

void add_wall_repulsion(Pedestrian * a)
{
	if(!U) return;
    int i;
    Vector * repulsion_points  = PyMem_Malloc(w_count * sizeof(Vector));
    int rep_p_c = 0;
    Vector repulsion;

    rep_p_c = find_repultion_points(a, repulsion_points);

    for(i = 0; i < rep_p_c; i++) {
        repulsion = calculate_wall_repulsion(a, repulsion_points[i]);
        vector_iadd(&a->acceleration, &repulsion);
    }


    PyMem_Free(repulsion_points);
}

int find_repultion_points(Pedestrian * a, Vector repulsion_points[])
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
			// P = A + AB*L/|AB|
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
            if(vector_equals(possible_endpoints[i], used_endpoints[j])) {
                use_e = 0;
            }
        }
        if(use_e) {
			// Keep track of whether the endpoint is free-floating, i.e. if
			// it is shared with another wall.
			int free_e = 1;
			for(j = 0; j < pos_e_c; j++) {
				if(i != j && 
						vector_equals(possible_endpoints[i],
							possible_endpoints[j])) {
					free_e = 0;
				}
			}
			// Endpoints that are free-floating (i.e. sides of doorways) are
			// only considered for repulsion if they are closer to the pedestrian
			// than the pedestrian's radius. This allows pedestrians to pass more
			// freely through doorways.
			if(!free_e || 
					vector_length(vector_sub(a->position,
							possible_endpoints[i])) < a->radius) {
				repulsion_points[rep_p_c++] = possible_endpoints[i];
				used_endpoints[use_e_c++] = possible_endpoints[i];
			}
        }
    }

    PyMem_Free(used_endpoints);
    PyMem_Free(possible_endpoints);

    return rep_p_c;
}

Vector calculate_wall_repulsion(Pedestrian * a, Vector repulsion_point)
{
    Vector repulsion_vector = vector_sub(a->position, repulsion_point);
    double repulsion_length = vector_length(repulsion_vector);
	vector_unitise_c(&repulsion_vector, repulsion_length);

	double repulsion_force = (1/a->radius) * U * exp(-repulsion_length/a->radius);

	vector_imul(&repulsion_vector, repulsion_force);

    return repulsion_vector;
}

void update_position(Pedestrian * a)
{
    Vector delta_p;

    delta_p.x = a->velocity.x * timestep + 0.5 * a->acceleration.x * pow(timestep, 2);
    delta_p.y = a->velocity.y * timestep + 0.5 * a->acceleration.y * pow(timestep, 2);


    vector_iadd(&a->position, &delta_p);
	a->velocity = vector_add(a->velocity,
			vector_mul(a->acceleration, timestep));
    a->time += timestep;

	if(a->flowline_time < 0) {
        if(vector_projection_distance(
					flowline[0], flowline[1], a->position) < a->radius) {
			a->flowline_time = a->time;
		}
	}
}

static int is_escaped(Pedestrian * a)
{
	double l = vector_length(vector_sub(a->target, a->position));
	if (l <= a->radius*2) return 1;
    if (a->position.x > ESCAPE_THRESHOLD || a->position.x < -ESCAPE_THRESHOLD
            || a->position.y > ESCAPE_THRESHOLD || a->position.y < -ESCAPE_THRESHOLD)
        return 1;
    return 0;
}


/*** Calculation part end ***/



// Threading variables
static Py_ssize_t threads_c;
#ifndef _WIN32
static pthread_t * threads;
static pthread_attr_t thread_attr;
#endif

static PyObject * update_pedestrians(PyObject * self, PyObject * args)
{

    // Since we are not touching any python objects in this part, 
    // we can release the global interpreter lock, to allow for multithreaded
    // goodness.
    Py_BEGIN_ALLOW_THREADS

        do_calculations();

    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

static PyObject * add_pedestrian(PyObject * self, PyObject * args)
{
    PyObject * p_pedestrian;
    int i = a_count;

    PyArg_ParseTuple(args, "O:add_pedestrians", &p_pedestrian);

	update_a_count(a_count+1);
	pedestrian_from_pyobject(p_pedestrian, &pedestrians[i]);

    Py_RETURN_NONE;
}

static PyObject * a_property(PyObject * self, PyObject * args)
{
    Py_ssize_t i;
	char * property;

    PyArg_ParseTuple(args, "is:a_property", &i, &property);


	if(i > a_count) {
		PyErr_SetString(PyExc_KeyError, NULL);
		return NULL;
	}

	if(strcmp(property, "position") == 0) {
		return Py_BuildValue("dd", 
				pedestrians[i].position.x, pedestrians[i].position.y);
	} else if(strcmp(property, "radius") == 0) {
		return PyFloat_FromDouble(pedestrians[i].radius);
	} else if(strcmp(property, "velocity") == 0) {
		return PyFloat_FromDouble(vector_length(pedestrians[i].velocity));
	} else if(strcmp(property, "flowline_time") == 0) {
		return PyFloat_FromDouble(pedestrians[i].flowline_time);
	} else if(strcmp(property, "target") == 0) {
		return Py_BuildValue("dd", 
				pedestrians[i].target.x, pedestrians[i].target.y);
	}

	PyErr_SetString(PyExc_AttributeError, property);
	return NULL;
}

static PyObject * set_parameters(PyObject * self, PyObject * args)
{
	PyObject * o, * p_walls, *p_flowline;
    PyArg_ParseTuple(args, "O:set_parameters", &o);

    A           = double_from_attribute(o, "A");
    B           = double_from_attribute(o, "B");
    U           = double_from_attribute(o, "U");
    lambda      = double_from_attribute(o, "lambda");
    timestep    = double_from_attribute(o, "timestep");

    p_walls     = PyDict_GetItemString(o, "walls");
    p_flowline  = PyDict_GetItemString(o, "flowrate_line");

	flowline[0].x = PyFloat_AsDouble(PyTuple_GetItem(p_flowline, 0));
	flowline[0].y = PyFloat_AsDouble(PyTuple_GetItem(p_flowline, 1));
	flowline[1].x = PyFloat_AsDouble(PyTuple_GetItem(p_flowline, 2));
	flowline[1].y = PyFloat_AsDouble(PyTuple_GetItem(p_flowline, 3));

    init_walls(p_walls);
	update_a_count(0);

    Py_RETURN_NONE;
}

static void do_calculations()
{
    int i, rc;
    void * status;
#ifndef _WIN32
    if(threads_c > 1) {
        Part * parts;
        parts = PyMem_Malloc(threads_c * sizeof(Part));
        int part_len = a_count / threads_c;
        for(i = 0; i < threads_c; i++) {
            parts[i].start = i*part_len;
            parts[i].end = (i+1)*part_len;
        }
        parts[threads_c-1].end += a_count % threads_c;

        for(i = 0; i < threads_c; i++) {
            rc = pthread_create(&threads[i], NULL, 
                    do_calculation_part, (void *) &parts[i]);
        }

        for(i = 0; i < threads_c; i++) {
            pthread_join(threads[i], &status);
        }
    } else {
#endif
        Part p = {0, a_count};
        do_calculation_part(&p);
#ifndef _WIN32
    }
#endif

    for(i = 0; i < a_count; i++) {
        update_position(&pedestrians[i]);
    }

	check_escapes();
}

static void do_calculation_part(Part * p)
{
    int i,j;
    for(i = p->start; i < p->end; i++) {
        calculate_forces(i);
    }
#ifndef _WIN32
    if(threads_c > 1) pthread_exit(NULL);
#endif
}

static void check_escapes()
{
	int i, j;

	for(i = 0, j = 0; i < a_count; i++) {
		if(!is_escaped(&pedestrians[i])) {
			pedestrians[j++] = pedestrians[i];
		}
	}

	if(i!=j) update_a_count(a_count - (i-j));

}

static void update_a_count(Py_ssize_t count)
{
	if(count == a_count) return;

	a_count = count;
	pedestrians = PyMem_Realloc(pedestrians, a_count * sizeof(Pedestrian));

	PyObject * tmp = PyInt_FromSsize_t(a_count);
    PyDict_SetItemString(module_dict, "a_count", tmp);
	Py_DECREF(tmp);

}

static Pedestrian pedestrian_from_pyobject(PyObject * o, Pedestrian * a)
{
    a->radius                   = double_from_attribute(o, "radius");
    a->time                     = double_from_attribute(o, "time");
    a->initial_desired_velocity = double_from_attribute(o, "initial_desired_velocity");
    a->max_velocity             = double_from_attribute(o, "max_velocity");
    a->relax_time               = double_from_attribute(o, "relax_time");

	a->flowline_time       = -1;


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
    PyObject * o2 = PyDict_GetItemString(o, name);
    double result = PyFloat_AsDouble(o2);
    return result;
}

static Vector vector_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyDict_GetItemString(o, name);
    Vector result = vector_from_pyobject(o2);
    return result;
}

static Vector vector_from_pyobject(PyObject * o)
{
    Vector v;

    PyObject * x = PySequence_GetItem(o, 0);
    PyObject * y = PySequence_GetItem(o, 1);
    v.x = PyFloat_AsDouble(x);
    v.y = PyFloat_AsDouble(y);

    Py_DECREF(x);
    Py_DECREF(y);

    return v;
}

static PyMethodDef OptimisedMethods[] = {
    {"update_pedestrians", update_pedestrians, METH_VARARGS, 
        "Calculate the acceleration of an pedestrian"},
    {"add_pedestrian", add_pedestrian, METH_VARARGS, 
        "Add an pedestrian to the list"},
    {"a_property", a_property, METH_VARARGS, 
        "Get a property for an pedestrian"},
    {"set_parameters", set_parameters, METH_VARARGS, 
        "Set simulation parameters"},
};

PyMODINIT_FUNC initoptimised(void)
{
    PyObject * c_module;

	PyObject * m, tmp;
    m = Py_InitModule("optimised", OptimisedMethods);
    module_dict = PyModule_GetDict(m);

    a_count  = -1;
    pedestrians   = NULL;
    A        = 0;
    B        = 0;
    lambda   = 0;
    timestep = 0;

	update_a_count(0);

    Py_AtExit(cleanup);

    c_module    = PyImport_ImportModule("constants");
    threads_c = ssize_t_from_attribute(c_module, "threads");

    Py_DECREF(c_module);

#ifndef _WIN32
    if(threads_c > 1) init_threads();
#endif
}

static void init_walls(PyObject * p_walls)
{
    int i;
    w_count = PyList_Size(p_walls);
    walls    = PyMem_Realloc(walls, w_count * sizeof(Wall));
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
#ifndef _WIN32
    if(threads_c > 1) destroy_threads();
#endif
}

static void init_threads()
{
#ifndef _WIN32
    threads = PyMem_Malloc(threads_c * sizeof(pthread_t));
    pthread_attr_init(&thread_attr);
    pthread_attr_setdetachstate(&thread_attr, PTHREAD_CREATE_JOINABLE);
#endif

}

static void destroy_threads()
{
#ifndef _WIN32
    pthread_attr_destroy(&thread_attr);
    PyMem_Free(threads);
#endif
}
