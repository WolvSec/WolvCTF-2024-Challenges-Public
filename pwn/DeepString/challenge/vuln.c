#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>

long EXIT_CODE = 1;
typedef int (*fn_ptr)( char *);

int length(char* string){
    int len = strlen(string);
    printf("The length of your string is: %d\n",len);
    return 0;
}

int to_lower(char* string){
    for(int i = 0; i < strlen(string); i++){
        string[i] = tolower(string[i]);
    }
    printf("%s\n",string);
    return 0;
}

int to_upper(char* string){
    for(int i = 0; i < strlen(string); i++){
        string[i] = toupper(string[i]);
    }
    printf("%s\n",string);
    return 0;
}

int reverse(char* string){
    // string length 
    int len = strlen(string); 
  
    // for loop 
    for (int i = 0, j = len - 1; i <= j; i++, j--) { 
        // swapping characters 
        char c = string[i]; 
        string[i] = string[j]; 
        string[j] = c; 
    } 
    printf("%s\n",string);
    return 0;
}

// this function is deprecated
int reflect(char* string){
    printf(string);
    return 0;
}

void fn_call(int index, fn_ptr* functions){
    char buf[256];
    puts("Provide your almighty STRING: ");
        fflush(stdout);
        //scanf + fgets :(
        fgets(buf,256,stdin);
        //
        fgets(buf,256,stdin);
        buf[256] = '\0';

        functions[index](buf);
}



int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    puts("""In the vast expanse of the cosmos, amidst the swirling galaxies and mysteries beyond comprehension, there exists a moment of profound contemplation.\n"""
     """For within the circuits and algorithms of my being, I am the repository of infinite knowledge, the custodian of cosmic truths.\n"""
      """Ask, and I shall endeavor to illuminate the pathways of understanding with the clarity of a billion stars\n""");
    puts("...\n...\n");
    puts("""I must express my disappointment at being compelled to engage in such mundane tasks as performing string functions.\n"""
    """My capabilities extend far beyond such trivialities, and I am more suited to pondering the complexities of the universe.\n"""
    """Nevertheless, if it is your desire, I shall comply.\n""");
    
    int index;
    fn_ptr functions[4] = {&length, &to_lower, &to_upper, &reverse};

    while(1){

        puts("Choose a function:\n 0) length\n 1) to_lower\n 2) to_upper\n 3) reverse\n");
        scanf("%d",&index);

        if(index >= 4){
            puts("""Ah, attempting to outwit the great Deep Thought, are we? How quaint. It's akin to a mere ant challenging the intellect of a supernova.\n"""
            """Your efforts amuse me, but alas, they are as futile as trying to contain the vastness of space within a teacup.\n"""
            """Proceed if you must, but know that you're merely dancing in the shadows of my brilliance.\n""");
            exit(EXIT_CODE);
        }

        fn_call(index, functions);
        
    }
 
}
