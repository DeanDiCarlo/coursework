#include <iostream>

int main() {
    long long a = 1, b = 2, c = 3;
    for (int i = 0; i < 10000000; i++) {
        a += b;
        a *= 2;
        c -= 1; 
        a *= 2; 
    }
    std::cout << a << "\n" << c;
    return 0;
}