#include <iostream>
#include <string>

using namespace std; // uwu


void print (string context) {
    cout << context << endl;
}
void print (int context) {
    cout << context << endl;
}

class Graph
{    
public:
    string board;
    int visitedNodes = 0;
    
    int * get_child_vertices (int board){
        return {0};
    }
};




int main() {
    // Add the Graph object
    // add the BFS search
    int biggest = 1000000000;
    cout << biggest << endl;
    return 0;
}