#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;

const int INITIAL_STOCK = 115;
const int GOODWILL_LOSS = 2;
const int UNIT_LOSS = 16;
const int ORDER_COST = 75;
const int ORDER_LAG = 3;
const double CARRYING_COST = .75;

int main() {
    int n, P, Q, demand, stock, ordered, restockDate;
    double cost;
    stock = INITIAL_STOCK, cost = 0, restockDate = -1, ordered = 0;
    cin >> n >> P >> Q;
    for(int day = 0; day < n; day++) {
        // day
        if(day == restockDate) {
            stock += Q;
            ordered = 0;
            restockDate = -1;
        }
        cin >> demand;
        if(demand > stock) {
            cost += (UNIT_LOSS + GOODWILL_LOSS) * (demand - stock);
            stock = 0;
        } else {
            stock -= demand;
        }
        
        // night
        if(stock + ordered <= P) {
            restockDate = day + ORDER_LAG;
            ordered = Q;
            cost += ORDER_COST;
        }
        cost += stock * CARRYING_COST;
    }
    cout << cost;
    return 0;
}
