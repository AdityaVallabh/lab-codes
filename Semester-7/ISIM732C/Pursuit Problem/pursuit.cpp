#include <stdio.h>
#include <math.h>

const int SPEED = 20;
const int RANGE = 10;

double getDistance(double u, double v, double x, double y) {
    return sqrt((u-x)*(u-x) + (v-y)*(v-y));
}

int main() {
    int n;
    double u, v, x, y, distance;
    scanf("%d%lf%lf", &n, &u, &v);
    for(int i = 0; i <= n; i++) {
        scanf("%lf%lf", &x, &y);
        distance = getDistance(u, v, x, y);
        if(distance <= RANGE) {
            printf("%d\n%.2lf", i, distance);
            return 0;
        }
        u += SPEED * (x - u)/distance;
        v += SPEED * (y - v)/distance;
    }
    printf("-1");
    return 0;
}
