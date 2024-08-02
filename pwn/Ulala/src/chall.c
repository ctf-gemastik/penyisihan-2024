#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SONGS 100
#define MAX_NAME_LENGTH 100

typedef struct {
    char title[MAX_NAME_LENGTH];
    char artist[MAX_NAME_LENGTH];
    int duration; // duration in seconds
} Song;

int song_count = 0; // Global variable to keep track of the number of songs

int readint(){
    char buf[0x10];
    return atoi(fgets(buf,0x10,stdin));
}

void addSong(Song playlist[]) {
    if (song_count >= MAX_SONGS) {
        printf("Playlist is full. Cannot add more songs.\n");
        return;
    }

    printf("Enter song title: ");
    fgets(playlist[song_count].title, 0x100, stdin);
    playlist[song_count].title[strcspn(playlist[song_count].title, "\n")] = '\0'; // Remove trailing newline

    printf("Enter artist name: ");
    fgets(playlist[song_count].artist, 0x100, stdin);
    playlist[song_count].artist[strcspn(playlist[song_count].artist, "\n")] = '\0'; // Remove trailing newline

    printf("Enter duration (in seconds): ");
    playlist[song_count].duration = readint();

    song_count++;
    printf("Song added successfully.\n");
}

void deleteSong(Song playlist[]) {
    if (song_count == 0) {
        printf("No songs to delete.\n");
        return;
    }

    int index;
    printf("Enter the number of the song to delete: ");
    index = readint();
 
    if (index < 1 || index > song_count) {
        printf("Invalid song number.\n");
        return;
    }

    // Use memset to clear the deleted song
    memset(&playlist[index - 1], 0, sizeof(Song));

    for (int i = index - 1; i < song_count - 1; i++) {
        playlist[i] = playlist[i + 1];
    }

    // Use memset to clear the last song
    memset(&playlist[song_count - 1], 0, sizeof(Song));
    
    song_count--;
    printf("Song deleted successfully.\n");
}

void displayPlaylist(Song playlist[]) {
    if (song_count == 0) {
        printf("Playlist is empty.\n");
        return;
    }

    printf("Playlist:\n");
    for (int i = 0; i < song_count; i++) {
        printf("%d. %s - %s (%d seconds)\n", i + 1, playlist[i].title, playlist[i].artist, playlist[i].duration);
    }
}

void displayMenu() {
    printf("Menu:\n");
    printf("1. Add Song\n");
    printf("2. Delete Song\n");
    printf("3. View Songs\n");
    printf("4. Exit\n");
}

void init()
{
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    __asm__("mov %rbp, %rdi");
}

int main() {
    init();
    int choice;
    Song playlist[MAX_SONGS];
    while (1) {
        displayMenu();
        printf("Enter your choice: ");
        choice = readint();

        switch (choice) {
            case 1:
                addSong(playlist);
                break;
            case 2:
                deleteSong(playlist);
                break;
            case 3:
                displayPlaylist(playlist);
                break;
            case 4:
                printf("Exiting the program.\n");
                return;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}