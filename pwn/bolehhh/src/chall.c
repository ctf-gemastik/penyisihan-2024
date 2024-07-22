#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NOTEBOOKS 10
#define MAX_TITLE_LENGTH 64
#define MAX_CONTENT_LENGTH 128

typedef struct {
    char title[MAX_TITLE_LENGTH];
    char content[MAX_CONTENT_LENGTH];
} Notebook;


Notebook notebooks[MAX_NOTEBOOKS];
int notebookCount = 0;

int readint(){
    char buf[0x10];
    return atoi(fgets(buf,0x10,stdin));
}

void addNotebook() {
    if (notebookCount >= MAX_NOTEBOOKS) {
        printf("Maximum number of notebooks reached!\n");
        return;
    }

    int index;
    printf("Enter notebook index: ");
    index = readint();
    if (*notebooks[index].title || index < 0 ) {
        printf("Notebook index already exists!\n");
        return;
    }

    Notebook notebook;
    printf("Enter notebook title: ");
    fgets(notebook.title, MAX_TITLE_LENGTH, stdin);
    
    printf("Enter notebook content: ");
    fgets(notebook.content, MAX_CONTENT_LENGTH, stdin);

    notebooks[index] = notebook;
    notebookCount = notebookCount+1;
    printf("Notebook added successfully!\n");
}

void removeNotebook() {
    if (notebookCount == 0) {
        printf("No notebooks available!\n");
        return;
    }

    int index;
    printf("Enter notebook index: ");
    index = readint();
    if ( index < 0 ) {
        printf("Notebook index cannot be negative !\n");
        return;
    }
    for (int i = 0; i < MAX_TITLE_LENGTH; ++i)
    {
        notebooks[index].title[i] = 0 ;
    }

    for (int i = 0; i < MAX_CONTENT_LENGTH; ++i)
    {
        notebooks[index].content[i] = 0 ;
    }

    // memset(notebooks[index].title, '\0', MAX_TITLE_LENGTH); 
    // memset(notebooks[index].content, '\0', MAX_CONTENT_LENGTH); 
    printf("Notebook removed successfully!\n");
}

void addFeedback() {

    char feedback[64];
    printf("Enter feedback: ");
    gets(feedback);

    // printf("Feedback added successfully!\n");
}
void init(){
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
}

int main() {
    init();
    int choice;
    while (1) {
        printf("\nSimple Notebook Application\n");
        printf("1. Add Notebook\n");
        printf("2. Remove Notebook\n");
        printf("3. Add Feedback\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        // scanf("%d", &choice);
        choice = readint();

        switch (choice) {
            case 1:
                addNotebook();
                break;
            case 2:
                removeNotebook();
                break;
            case 3:
                addFeedback();
                break;
            case 4:
                exit(0);
            default:
                printf("Invalid choice! Please try again.\n");
        }
    }

    return 0;
}