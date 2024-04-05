#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int NUM_COMMENTS = 0;

void opts();
void lookPost();
void makeComment();

int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    puts("\n" 
    "██████╗ ██╗   ██╗████████╗███████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗      ██████╗ ██╗    ██╗\n"
    "██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║     ██╔═══██╗██║    ██║\n"
    "██████╔╝ ╚████╔╝    ██║   █████╗  ██║   ██║██║   ██║█████╗  ██████╔╝█████╗  ██║     ██║   ██║██║ █╗ ██║\n"
    "██╔══██╗  ╚██╔╝     ██║   ██╔══╝  ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══╝  ██║     ██║   ██║██║███╗██║\n"
    "██████╔╝   ██║      ██║   ███████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██║     ███████╗╚██████╔╝╚███╔███╔╝\n"
    "╚═════╝    ╚═╝      ╚═╝   ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ \n"
    ""); 
    puts("                                                   \n"                  
         "                                  (((((            \n"                   
         "                                   (((((,          \n"                     
         "                            (        (((((*        \n"                     
         "                          /(((((      /(((((       \n"                     
         "                            ((((((((    /(((((     \n"                     
         "                               (((((((*   ((((((   \n"                     
         "                     .(((,        (((((((,  (((((( \n"                     
         "                    *((((((((((      (((((((# (    \n"                     
         "                         (((((((((((    ((((#      \n"                     
         "                               ((((((((((*         \n"                     
         "                  ((((((((          (((((          \n"                     
         "                  (((((((((((((((((((/             \n"                     
         "         %%%%             ,,((((((((((((   ,%%%%   \n"                     
         "         %%%%                         .    ,%%%%   \n"                     
         "         %%%%    ((((((((((((((((((((((    ,%%%%   \n"                     
         "         %%%%    ((((((((((((((((((((((    ,%%%%   \n"                     
         "         %%%%                              ,%%%%   \n"                     
         "         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   \n"                     
         "         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   \n" );
    while(1){
        opts();
    }
}

void opts(){
    int chosen_option;
    puts("Welcome! What do you want to do?\n");
    puts("1) LOOK AT A POST\n");
    puts("2) MAKE A COMMENT\n");
    puts("3) EXIT\n");
    scanf("%d",&chosen_option);
    getchar();  
    switch(chosen_option){
        case 1:
            lookPost();
            return;
            break;
        case 2:
            makeComment();
            break;
        case 3:
            exit(0);
        default: 
            printf("Not a valid option. Please try again.\n");
            break;
    }
}

void lookPost(){
    char buf[256];
    puts("Select one of the following: \n");
    printf("1) Why do hackers prefer dark mode while coding?\n");
    puts("\n");
    printf("2) The Ultimate Guide to Hacking - Secure Your Coffee Machine's Firmware!\n");
    puts("\n");
    printf("3) The Secret Society of Silent Print Statements - Debugging in Stealth Mode\n");
    puts("\n");
    

    fflush(stdout);
    read(0,buf,257);
    //printf("READ: %s",buf);
    //fgets(buf, 257, stdin); doesnt work cuz null terminator

    if(buf[0] == '1'){
        puts("------------------------------------------------------------------------------------\n");
        puts("Greetings fellow code enigmas! Have you ever wondered why hackers have an undeniable affinity for dark mode? Join our cryptic investigation as we unveil the hidden secrets behind this nocturnal coding preference. Share your theories on whether it's for stealth, enhanced focus, or just a love for stylish, mysterious aesthetics. Let the dark secrets be revealed!\n");
        puts("------------------------------------------------------------------------------------\n");    
    }

    else if(buf[0] == '2'){
        puts("------------------------------------------------------------------------------------\n");
        puts("Hey fellow hackers, I recently discovered a groundbreaking technique to secure my coffee machine's firmware. It involves a mix of reverse engineering, coffee bean encryption, and a dash of caffeine-based encryption keys. Let's share our innovative approaches to make our appliances hacker-proof!\n");
        puts("------------------------------------------------------------------------------------\n");
 
    }

    else if(buf[0] == '3'){
        puts("------------------------------------------------------------------------------------\n");
        puts("Greetings clandestine coders! Unveil the mysteries of stealth debugging with the Silent Print Statement Society. Share your experiences on embedding print statements so discreetly that even the logs remain silent. Let's discuss the art of leaving no trace while unraveling the secrets of our code in the shadows!\n");
        puts("------------------------------------------------------------------------------------\n");

    }
    return;
}

void makeComment(){
    if(NUM_COMMENTS != 0){
        puts("You can only leave one comment\n");
        return;
    }
    char buf[256];
    puts("Please write your comment below: \n");
    fgets(buf,256,stdin);
    printf("Your comment is the following: \n");
    printf(buf);
    NUM_COMMENTS++;
    return;
}
