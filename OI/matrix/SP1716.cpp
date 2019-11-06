#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <deque>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <string>
#include <utility>
#include <vector>
#define rep(i, l, r) for (int i = (l); i <= (r); ++i)
#define per(i, l, r) for (int i = (l); i >= (r); --i)
using std::cerr;
using std::cin;
using std::cout;
using std::endl;
using std::make_pair;
using std::max;
using std::pair;
typedef pair<int, int> pii;
typedef long long ll;
typedef unsigned int ui;

const int inf = 0x3f3f3f3f;

struct Mat {
    int a[3][3];
    Mat() { memset(a, 0xcf, sizeof a); }
    int* operator[](int x) { return a[x]; }
    Mat operator*(Mat rhs) {
        Mat ret;
        rep(i, 0, 2) rep(j, 0, 2) rep(k, 0, 2) ret[i][j] =
            max(ret[i][j], a[i][k] + rhs[k][j]);
        return ret;
    }
    void set(int x) {
        a[0][0] = a[0][1] = a[2][0] = a[2][1] = x;
        a[0][2] = a[1][0] = a[1][2] = -inf;
        a[1][1] = a[2][2] = 0;
    }
    void print() {
        rep(i, 0, 2) {
            rep(j, 0, 2) cerr << a[i][j] << ' ';
            cerr << endl;
        }
    }
};

const int N = 50010;

struct Node {
    int l, r;
    Node *ls, *rs;
    Mat m;
} T[N * 4];
int cnt = 0;

void build(Node*& c, int l, int r) {
    c = &T[cnt++];
    c->l = l, c->r = r;
    if (l == r) {
        int x;
        cin >> x;
        c->m.set(x);
        return;
    }
    int mid = (l + r) / 2;
    build(c->ls, l, mid), build(c->rs, mid + 1, r);
    c->m = c->ls->m * c->rs->m;
}

int L, R;
Mat ask(Node* c) {
    // cerr << c->l << ' ' << c->r << ' ' << L << ' ' << R << endl;
    // assert(!(c->r < L || R < c->l));

    if (L <= c->l && c->r <= R) return c->m;
    int mid = c->ls->r;
    if (R <= mid) {
        return ask(c->ls);
    } else if (L > mid) {
        return ask(c->rs);
    } else {
        return ask(c->ls) * ask(c->rs);
    }
}

int P, X;
void e(Node* c) {
    if (c->l == c->r) {
        c->m.set(X);
        return;
    }
    if (P <= c->ls->r)
        e(c->ls);
    else
        e(c->rs);
    c->m = c->ls->m * c->rs->m;
}

int main() {
#ifdef LOCAL
    freopen("input", "r", stdin);
#endif
    std::ios::sync_with_stdio(false);
    cout.tie(0);
    int n, m;
    cin >> n;
    Node* rt = nullptr;
    build(rt, 1, n);
    // cerr << "build over" << endl;
    cin >> m;
    while (m--) {
        int opt;
        cin >> opt;
        if (opt == 0) {
            cin >> P >> X;
            e(rt);
        } else {
            cin >> L >> R;
            // cout << ask(rt)[]
            Mat tmp = ask(rt);
            cout << max(tmp[0][1], tmp[2][1]) << endl;
        }
    }
    return 0;
}