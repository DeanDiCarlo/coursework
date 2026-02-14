#include <iostream>

int main() {
    long long a = 0;
    for (int i = 0; i < 10000000; i++) {
        a += 1;
    }
    std::cout << a << "\n";
    return 0;
}