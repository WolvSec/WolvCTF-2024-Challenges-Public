#include <stdio.h>
#include <string.h>
#include <unistd.h>

char flag[] = "wctf{n1c3_oNe_y0u_Found_m3}";

int main(void) 
{
    char buff[1024] = {0};

    printf("How are you today?\n");
    scanf("%s", buff);
    sleep(1.5);
    if (!strcmp(buff, "good")) {
        printf("Glad to hear that :)\n");
    }
    else if (!strcmp(buff, "bad")) {
        printf("Sorry to hear that :(\n");

    }
    else {
        printf("Not sure how to react to that :/\n");
    }
    sleep(1.5);

    printf("Did you checkout our cool sponsors?\n");
    scanf("%s", buff);
    sleep(1.5);
    if (!strcmp(buff, "yes")) {
        printf("Awesome!\n");
    }
    else {
        printf("You should totally check them out!\n");

    }
    sleep(1.5);
    
    printf("I think I am forgetting something...\n");
    sleep(2);
    printf("Oh yea the flag!\n");
    sleep(1.5);
    printf("But where did I put it...\n");
    sleep(3);
    printf("I know its in here somewhere.\n");
    sleep(3);
    printf("Dratts! Can you help me find it?\n");
    sleep(1);
    printf("I swear its around here somewhere.\n");
    sleep(5);

    return 0;
}