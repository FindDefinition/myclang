__global__ void add(float* addr, size_t size){
    addr[threadIdx.x] += 1;
}

