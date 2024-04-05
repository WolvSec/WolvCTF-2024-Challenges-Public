#ifndef RUNNER_H
#define RUNNER_H

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <vector>

// Define the CScript Engine
/**
 * @def The CScript engine is fairly simple and defined as follows:
 * HEAP OPERATIONS:
 * 1. Store(obj) - Manually the obj in the heap
 * 2. Release() - Manually release the obj from the heap
 * 3. Clear() - Manually clear the heap
 * @def The CScript language also implements some runtime objects for the users convenience:
 * TODO:
    * 1. Timer - A timer object that can be used to perform operations asynchronously
    * 2. String - A generic string that can be used to store data
    * 3. Number - A generic number that can be used to store data
    * 4. Boolean - A generic boolean that can be used to store data
    * 5. Function - A generic function that can be used to store data
 */

// Define the FIXME language heap operations
#define STORE 1
#define RELEASE 2
#define CLEAR 3
#define PRINT 4

// Define the FIXME language runtime objects
#define STRING 1
#define INTEGER 2
#define BOOLEAN 3
#define TIMER 4
#define OBJECT 5

typedef struct __attribute__((packed)) {
   size_t size;
   uint8_t type;
   uint8_t *data;
   void (*print)(void *);
} object_t;

typedef struct __attribute__((packed)) {
   uint8_t command;
   void *arg1;
} command_t;

uint32_t execute(command_t *, std::vector<void *> &);

#endif // RUNNER_H
