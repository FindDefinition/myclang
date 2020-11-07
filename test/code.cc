#include <iostream>
#include <sstream>
template <typename T1, typename T2>
struct D{
  static constexpr int V = 0;
  T1 add(T1 x, T1 y){
    return x + y + V;
  }
};
struct E;
struct E {
  static constexpr int V = 12; 
};

// #include <iostream>
namespace C {

template <typename T>
struct B {
  int a = 5;
  int b = a + 3;
};

template <typename T>
class A {

public:
  T b = 5;
  B<T> c;
  ~A(){
    std::cout << "???" << std::endl;
  }
  T add(T x, T y){
    return x + y + b;
  }
};

template <>
class A<float> {

public:
  float b = 8;
  B<float> c;

  float add(float x, float y){
    return x + y + b;
  }
};
}
template <typename T1>
struct D<float, T1>{
  T1 add(T1 x, T1 y){
    return x + y + V;
  }
  static constexpr int V = 5;
};


int main(){  
  using A_t = C::A<float>;
    C::A<float> a = C::A<float>();
    auto b = C::B<float>();
    auto c = D<float, int>::V;
    D<double, int> d;
    D<float, int> v_partial;
    using TX = D<float, int>;
    a.add(3, 6);
    v_partial.add(3, 6);
    b.a;
    D<double, int> v_partial2; 
    v_partial2.add(4, 5); 

    // auto c = std::make_tuple(a, b);
    // if constexpr (false){
    //     auto [a_, b_] = c;

    // }
    // std::cout << a.b << b.a << std::endl;
}
