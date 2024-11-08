/* Final_Motor_Move.c */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

/* Constants to define GPIO paths and settings */
#define ROOT_GPIO_DEVICES "/sys/class/gpio"  // Base directory for GPIO control
#define EXPORT "export"			     // Path to export GPIO pins
#define UNEXPORT "unexport"		     // Path to unexport GPIO pins
#define DIRECTION "direction"	             // Path for setting GPIO direction
#define VALUE "value"		             // Path for writing values to GPIO
#define OUT 0			             // Constant for output direction
#define OUT_STR "out"			     // String to set direction to output
#define STR_LEN 256			     // Buffer size for file paths
#define GPIO_PIN_CW 17 			     // GPIO17 pin for clockwise rotation
#define GPIO_PIN_CCW 27			     // GPIO27 pin for counterclockwise rotation

/* Function declarations */
int GPIOInit(int);        // Function to initialize a GPIO pin
int GPIOSetDir(int, int); // Function to set direction of GPIO pin (output/input)
int GPIOWrite(int, int);  // Function to write a value (0 or 1) to GPIO pin
void runMotor(int);       // Function to run motor in a specified direction
void stopMotor();         // Function to stop the motor

/* Main program */
int main(void)
{
    // Initialize both GPIO pins for motor control
    if (GPIOInit(GPIO_PIN_CW) < 0 || GPIOInit(GPIO_PIN_CCW) < 0)
    {
        fprintf(stderr, "ERROR: Failed to initialize GPIO pins\n");
        return -1;
    }

    // Set both pins as output
    if (GPIOSetDir(GPIO_PIN_CW, OUT) < 0 || GPIOSetDir(GPIO_PIN_CCW, OUT) < 0)
    {
        fprintf(stderr, "ERROR: Failed to set direction for GPIO pins\n");
        return -1;
    }

    char command[10];  // Buffer to hold command input

    // Loop to continuously accept user commands for motor control
    while (1) {
        printf("Enter command (cw, ccw, stop): ");
        fgets(command, sizeof(command), stdin);  // Read user input

        // Check for command to run the motor
        if (strncmp(command, "cw", 2) == 0) {
            printf("Running motor clockwise\n");
            runMotor(1); // Pass 1 for clockwise rotation
        } else if (strncmp(command, "ccw", 3) == 0) {
            printf("Running motor counterclockwise\n");
            runMotor(0); // Pass 0 for counterclockwise rotation
        } else if (strncmp(command, "stop", 4) == 0) {
            printf("Stopping motor\n");
            stopMotor(); // Stop the motor
        } else {
            printf("Unknown command. Use 'cw', 'ccw', or 'stop'.\n");
        }
    }

    return 0;
}

/* GPIO initialization */
int GPIOInit(int iGPIONumber)
{
    char szAccessPath[STR_LEN];
    FILE *fOut;

    sprintf(szAccessPath, "%s/%s", ROOT_GPIO_DEVICES, EXPORT);
    if ((fOut = fopen(szAccessPath, "w")) == NULL)
    {
        fprintf(stderr, "ERROR: GPIOInit() -> fopen(%s,..)\n", szAccessPath);
        fprintf(stderr, "       error code %d (%s)\n", errno, strerror(errno));
        return -errno;
    }

    fprintf(fOut, "%d", iGPIONumber);
    fclose(fOut);
    return 0;
}

/* Set GPIO direction (output) */
int GPIOSetDir(int iGPIONumber, int iDataDirection)
{
    char szAccessPath[STR_LEN];
    FILE *fOut;

    sprintf(szAccessPath, "%s/gpio%d/%s", ROOT_GPIO_DEVICES, iGPIONumber, DIRECTION);
    if ((fOut = fopen(szAccessPath, "w")) == NULL)
    {
        fprintf(stderr, "ERROR: GPIOSetDir() -> fopen(%s,..)\n", szAccessPath);
        fprintf(stderr, "       error code %d (%s)\n", errno, strerror(errno));
        return -errno;
    }

    if (iDataDirection == OUT)
    {
        fprintf(fOut, "%s", OUT_STR);
    }
    else
    {
        fclose(fOut);
        return -1;
    }

    fclose(fOut);
    return 0;
}

/* Write value to GPIO */
int GPIOWrite(int iGPIONumber, int iValue)
{
    char szAccessPath[STR_LEN];
    FILE *fOut;

    sprintf(szAccessPath, "%s/gpio%d/%s", ROOT_GPIO_DEVICES, iGPIONumber, VALUE);
    if ((fOut = fopen(szAccessPath, "w")) == NULL)
    {
        fprintf(stderr, "ERROR: GPIOWrite() -> fopen(%s,..)\n", szAccessPath);
        fprintf(stderr, "       error code %d (%s)\n", errno, strerror(errno));
        return -errno;
    }

    fprintf(fOut, "%d", iValue); // Writing 0 or 1 directly
    fclose(fOut);
    return 0;
}

/* Run the motor */
void runMotor(int direction)
{
    if (direction == 1) // Clockwise
    {
        GPIOWrite(GPIO_PIN_CW, 1);
        GPIOWrite(GPIO_PIN_CCW, 0);
    }
    else if (direction == 0) // Counterclockwise
    {
        GPIOWrite(GPIO_PIN_CW, 0);
        GPIOWrite(GPIO_PIN_CCW, 1);
    }
}

/* Stop the motor */
void stopMotor()
{
    GPIOWrite(GPIO_PIN_CW, 0);
    GPIOWrite(GPIO_PIN_CCW, 0);
}
