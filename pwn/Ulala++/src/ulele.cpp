#include <iostream>
#include <vector>
#include <cstring>
#include <unistd.h>
#include <seccomp.h>

#define MAX_STRING_SIZE 100
#define MAX_NOTES 200

class Note {
public:
    char* data;

    Note() {
        data = new char[MAX_STRING_SIZE];
    }

    ~Note() {
        delete[] data;
    }
};

class NoteManager {
public:
    std::vector<Note*> notes;

    NoteManager() {
        notes.reserve(MAX_NOTES);
    }

    ~NoteManager() {
        for (auto note : notes) {
            delete note;
        }
    }

    char* createNote() {
        Note* new_note = new Note();
        notes.push_back(new_note);
        return new_note->data;
    }

    char* fetchNote(uint8_t idx) {
        if (idx < notes.size() && notes[idx] != nullptr) {
            return notes[idx]->data;
        } else {
            std::cerr << "Note index out of range." << std::endl;
            exit(1);
        }
    }

    void destroyNote(uint8_t idx) {
        if (idx < notes.size() && notes[idx] != nullptr) {
            delete notes[idx]->data;
        } else {
            std::cerr << "Note index out of range." << std::endl;
            exit(1);
        }
    }
};

void worker(NoteManager& nm);
int menuSelect();
void oplan1(NoteManager& nm);
void oplan2(NoteManager& nm);
void oplan3(NoteManager& nm);
void init();

int main() {
    init();
    std::cout << "[[ LINZ_IS_HERE ]]" << std::endl;

    NoteManager nm;

    while (true) {
        worker(nm);
    }

    return 0;
}

void worker(NoteManager& nm) {
    while (true) {
        switch (menuSelect()) {
            case 1:
                oplan1(nm);
                break;
            case 2:
                oplan2(nm);
                break;
            case 3:
                oplan3(nm);
                break;
            case 4:
                std::cout << "Exit...." << std::endl;
                exit(0);
            default:
                exit(0);
        }
    }
}

int menuSelect() {
    int choice;
    std::cout << "1. Add" << std::endl;
    std::cout << "2. View" << std::endl;
    std::cout << "3. Destroy" << std::endl;
    std::cout << "4. Exit" << std::endl;
    std::cout << ">> ";

    while (std::cin >> choice) {
        if (choice >= 1 && choice <= 4) {
            return choice;
        }
    }
    exit(1);
}

void oplan1(NoteManager& nm) {
    std::cout << "Payload: ";
    char* payload = nm.createNote();
    std::memset(payload, 0, MAX_STRING_SIZE);
    read(0, payload, MAX_STRING_SIZE);
}

void oplan2(NoteManager& nm) {
    int idx;
    std::cout << "Index: ";
    std::cin >> idx;
    if (idx >= 0) {
        std::cout << "Data: " << nm.fetchNote(static_cast<uint8_t>(idx)) << std::endl;
    } else {
        exit(1);
    }
}

void oplan3(NoteManager& nm) {
    int idx;
    std::cout << "Enter the index of the note to destroy: ";
    std::cin >> idx;
    if (idx >= 0) {
        nm.destroyNote(static_cast<uint8_t>(idx));
        nm.notes[idx] = nullptr;
    } else {
        exit(1);
    }
}

void init() {
    scmp_filter_ctx ctx;
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(open),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(read),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(write),0);
    seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(getdents),0);
    seccomp_load(ctx);
}
