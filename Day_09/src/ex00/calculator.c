#include <Python.h>



static PyObject *add_function(PyObject *self, PyObject *args) {
    double a, b;
   if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }
    return Py_BuildValue("d", a+b);
}

static PyObject *sub_function(PyObject *self, PyObject *args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }
    return PyFloat_FromDouble(a - b);
}

static PyObject *mul_function(PyObject *self, PyObject *args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }
    return PyFloat_FromDouble(a * b);
}

static PyObject *div_function(PyObject *self, PyObject *args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }

    if (b == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "division by zero");
        return NULL;
    }
    return PyFloat_FromDouble(a / b);
}

static PyMethodDef Methods[] = {
    {"add", add_function, METH_VARARGS, "Add two numbers"},
    {"sub", sub_function, METH_VARARGS, "Sub two numbers"},
    {"mul", mul_function, METH_VARARGS, "Mul two numbers"},
    {"div", div_function, METH_VARARGS, "Div two numbers"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
    PyModuleDef_HEAD_INIT,
    "calc",
    "Calculate module",
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_calc(void) {
    return PyModule_Create(&Module);
}
