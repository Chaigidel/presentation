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
using std::pair;
typedef pair<int, int> pii;
typedef long long ll;
typedef unsigned int ui;
#define mod(x) (x) %= P;
const int N = 100010;
const int P = 1e9 + 7;
int n;
struct Change {
    ll a[2][2];
    Change() { a[0][0] = a[0][1] = a[1][0] = a[1][1] = 0; }
    ll* operator[](int x) { return a[x]; }
    Change operator*(Change rhs) {
        Change ret;
        mod(ret[0][0] = a[0][0] * rhs[0][0] + a[0][1] * rhs[1][0]);
        mod(ret[0][1] = a[0][0] * rhs[0][1] + a[0][1] * rhs[1][1]);
        mod(ret[1][0] = a[1][0] * rhs[0][0] + a[1][1] * rhs[1][0]);
        mod(ret[1][1] = a[1][0] * rhs[0][1] + a[1][1] * rhs[1][1]);
        return ret;
    }
    void print() {
        rep(i, 0, 1) {
            rep(j, 0, 1) cerr << a[i][j] << ' ';
            cerr << endl;
        }
    }
} f[51];
struct Status {
    ll a[2];
    ll& operator[](int x) { return a[x]; }
    Status() { a[0] = 0, a[1] = 1; }
    Status operator*(Change r) {
        Status ret;
        mod(ret[0] = a[0] * r[0][0] + a[1] * r[1][0]);
        mod(ret[1] = a[0] * r[0][1] + a[1] * r[1][1]);
        return ret;
    }
    Status& operator*=(Change r) {
        *this = (*this) * r;
        return *this;
    }
    void print() { cerr << a[0] << ' ' << a[1] << endl; }
};
const int I = 50;
struct Node {
    int l, r;
    ll tag;
    Status s;
    Node *ls, *rs;
} T[N * 4];
int cnt = 0, L, R, X;

void merge(Node* c) {
    mod(c->s[0] = c->ls->s[0] + c->rs->s[0]);
    mod(c->s[1] = c->ls->s[1] + c->rs->s[1]);
}

Change fst(ll n) {
    Change ret;
    ret[0][0] = ret[1][1] = 1;
    for (int i = I; (i >= 0) && n; --i) {
        if ((n >> i) & 1LL) {
            ret = ret * f[i];
        }
    }
    return ret;
}

void build(Node*& c, int l, int r) {
    c = &T[cnt++];
    c->l = l, c->r = r;
    if (l == r) {
        int a;
        cin >> a;
        c->s *= fst(a - 1);
        // cerr << l << ' ' << r << endl;
        // c->s.print();
        // cerr << "----" << endl;
        return;
    }
    int mid = (l + r) / 2;
    build(c->ls, l, mid), build(c->rs, mid + 1, r);
    merge(c);
}

void pre() {
    f[0][0][1] = f[0][1][0] = f[0][1][1] = 1;
    rep(i, 1, I) f[i] = f[i - 1] * f[i - 1];
}

void pd(Node* c) {
    c->ls->tag += c->tag, c->rs->tag += c->tag;
    Change t = fst(c->tag);
    c->ls->s *= t, c->rs->s *= t;
    c->tag = 0;
}

void edit(Node* c) {
    if (c->r < L || R < c->l) return;
    if (L <= c->l && c->r <= R) {
        c->tag += X;
        c->s *= fst(X);
        return;
    }
    pd(c);
    int mid = c->ls->r;
    if (R <= mid)
        edit(c->ls);
    else if (L > mid)
        edit(c->rs);
    else
        edit(c->ls), edit(c->rs);
    merge(c);
}

inline ll add(ll x, ll y) {
    ll t = x + y;
    return t >= P ? t - P : t;
}

ll ask(Node* c) {
    if (c->r < L || R < c->l) return 0;
    if (L <= c->l && c->r <= R) return c->s[1];
    pd(c);
    int mid = c->ls->r;
    if (R <= mid)
        return ask(c->ls);
    else if (L > mid)
        return ask(c->rs);
    else
        return add(ask(c->ls), ask(c->rs));
}

int main() {
#ifdef LOCAL
    freopen("input", "r", stdin);
#endif
    pre();
    std::ios::sync_with_stdio(false);
    cout.tie(0);
    int m;
    Status s;
    cin >> n >> m;
    Node* rt = nullptr;
    build(rt, 1, n);
    while (m--) {
        int opt;
        cin >> opt >> L >> R;
        if (opt == 1) {
            cin >> X;
            edit(rt);
        } else
            cout << ask(rt) << endl;
    }
    return 0;
}