#!/usr/bin/env python
#
# Provides PyMite's builtins module, __bi.
#
# Copyright 2002 Dean Hall.
#
# USAGE
# -----
#
# The builtins are loaded by the interpreter.
# The user must not import this module directly.
#
# LOG
# ---
#
# 2006/08/21    #28: Adapt native libs to use the changed func calls
# 2002/12/20    Added globals, locals, range.
# 2002/12/19    Created.
#


#### TODO
#ord, chr, hex, dir, reload, str, repr, tuple


#### CONSTS

C = "Copyright 2001 Dean W. Hall.  All rights reserved."


#### FUNCS

def globals():
    """__NATIVE__
    pPyObj_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        return PY_RET_EX_TYPE;
    }

    /* Return calling frame's globals dict  on stack*/
    pr = (pPyObj_t)NATIVE_GET_PFRAME()->fo_globals;
    NATIVE_SET_TOS(pr);
    
    return PY_RET_OK;
    """
    pass


def id(o):
    """__NATIVE__
    PyReturn_t retval;
    pPyObj_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        return PY_RET_EX_TYPE;
    }

    /* Return object's address as an int on the stack */
    retval = int_new((U16)NATIVE_GET_LOCAL(0), &pr);
    NATIVE_SET_TOS(pr);
    
    return retval;
    """
    pass


def len(s):
    """__NATIVE__
    PyReturn_t retval;
    pPyObj_t ps = C_NULL;
    pPyObj_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        return PY_RET_EX_TYPE;
    }

    /* Get first arg */
    ps = NATIVE_GET_LOCAL(0);

    /* Get the length of the arg based on its type */
    switch (ps->od.od_type)
    {
        case OBJ_TYPE_STR:
            retval = int_new(((pPyString_t)ps)->length, &pr);
            break;

        case OBJ_TYPE_TUP:
            retval = int_new(((pPyTuple_t)ps)->length, &pr);
            break;

        case OBJ_TYPE_LST:
            retval = int_new(((pPyList_t)ps)->length, &pr);
            break;

        case OBJ_TYPE_DIC:
            retval = int_new(((pPyDict_t)ps)->length, &pr);
            break;

        default:
            /* If not a string or sequence type, raise TypeError */
            retval = PY_RET_EX_TYPE;
    }

    NATIVE_SET_TOS(pr);
    return retval;
    """
    pass


def locals():
    """__NATIVE__
    pPyObj_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        return PY_RET_EX_TYPE;
    }

    /* Return calling frame's local attrs dict on the stack */
    pr = (pPyObj_t)NATIVE_GET_PFRAME()->fo_attrs;
    NATIVE_SET_TOS(pr);
    
    return PY_RET_OK;
    """
    pass


def map(f, s):
    """__NATIVE__
    PyReturn_t retval;
    pPyObj_t pf = C_NULL;
    pPyObj_t ps = C_NULL;
    pPyObj_t pr = C_NULL;
    S8 length = 0;
    S8 i = 0;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        return PY_RET_EX_TYPE;
    }

    /* Get args */
    pf = NATIVE_GET_LOCAL(0);
    ps = NATIVE_GET_LOCAL(1);

    /* If args are wrong type, raise TypeError */
    if (pf->od.od_type != OBJ_TYPE_FXN)
    {
        return PY_RET_EX_TYPE;
    }

    /* Get the sequence length based on type */
    switch (ps->od.od_type)
    {
        case OBJ_TYPE_TUP:
            length = ((pPyTuple_t)ps)->length;
            break;

        case OBJ_TYPE_LST:
            length = ((pPyList_t)ps)->length;
            break;

        case OBJ_TYPE_STR:
            length = ((pPyString_t)ps)->length;
            break;

        default:
            return PY_RET_EX_TYPE;
    }

    /* XXX: Do a dummy map, fill func with Nones */
    retval = list_new(&pr);
    PY_RETURN_IF_ERROR(retval);

    for (i = 0; i < length; i++)
    {
        retval = list_append(pr, PY_NONE);
        PY_RETURN_IF_ERROR(retval);
    }

    return retval;
    """
    pass


def range(a, b, c):
    """__NATIVE__
    PyReturn_t retval;
    pPyObj_t pa = C_NULL;
    pPyObj_t pb = C_NULL;
    pPyObj_t pc = C_NULL;
    pPyObj_t pi = C_NULL;
    pPyObj_t pr = C_NULL;
    U16 i = 0;

    switch (NATIVE_GET_NUM_ARGS())
    {
        case 1:
            pa = PY_ZERO;
            pb = NATIVE_GET_LOCAL(0);
            pc = PY_ONE;
            break;

        case 2:
            pa = NATIVE_GET_LOCAL(0);
            pb = NATIVE_GET_LOCAL(1);
            pc = PY_ONE;
            break;

        case 3:
            pa = NATIVE_GET_LOCAL(0);
            pb = NATIVE_GET_LOCAL(1);
            pc = NATIVE_GET_LOCAL(2);

            /* If 3rd arg is 0, ValueError */
            if (((pPyInt_t)pc)->val == 0)
            {
                return PY_RET_EX_VAL;
            }
            break;

        default:
            /* If wrong number of args, raise TypeError */
            return PY_RET_EX_TYPE;
    }

    /* Allocate list */
    retval = list_new(&pr);
    PY_RETURN_IF_ERROR(retval);

    /* Iterate depending on counting direction */
    if (((pPyInt_t)pc)->val > 0)
    {
        for (i = ((pPyInt_t)pa)->val;
             i < ((pPyInt_t)pb)->val;
             i += ((pPyInt_t)pc)->val)
        {
            retval = int_new(i, &pi);
            PY_RETURN_IF_ERROR(retval);

            retval = list_append(pr, pi);
            PY_RETURN_IF_ERROR(retval);
        }
    }
    else
    {
        for (i = ((pPyInt_t)pa)->val;
             i > ((pPyInt_t)pb)->val;
             i += ((pPyInt_t)pc)->val)
        {
            retval = int_new(i, &pi);
            PY_RETURN_IF_ERROR(retval);

            list_append(pr, pi);
            PY_RETURN_IF_ERROR(retval);
        }
    }

    /* Return list */
    NATIVE_SET_TOS(pr);
    return retval;
    """
    pass


def type(o):
    """__NATIVE__
    PyReturn_t retval;
    pPyObj_t po = C_NULL;
    pPyObj_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        return PY_RET_EX_TYPE;
    }

    /* Get arg */
    po = NATIVE_GET_LOCAL(0);

    /* Create int from type enum */
    retval = int_new(po->od.od_type, &pr);
    NATIVE_SET_TOS(pr);
    return retval;
    """
    pass