#include <unordered_map>
#include <unordered_set>
#include <deque>
#include <clang-c/Index.h>
#include <vector> 
#include <exception>
#include <regex>
#include <cstdint>
#include <iostream>
#define CODEAI_EXPORT 

using pointer_container_t = std::uintptr_t;

std::vector<CXCursor> get_cursor_children(const CXCursor& cu){
    std::vector<CXCursor> res;
    CXCursorVisitor visitor = [](CXCursor cursor,
                    CXCursor parent,
                    CXClientData client_data) -> CXChildVisitResult {
       if (clang_Cursor_isNull(cursor)){
           throw std::runtime_error("FIXME: Document this assertion in API");
       }
       auto& res_ = *(reinterpret_cast<decltype(res)*>(client_data));
       res_.push_back(cursor);
       return CXChildVisitResult::CXChildVisit_Continue;
    };
    clang_visitChildren(cu, visitor, reinterpret_cast<void*>(&res));
    return res;
}

using CXCursor_int_t = std::tuple<int64_t, int64_t, std::array<std::uintptr_t, 3>>;


std::unordered_map<std::string, std::unordered_map<int64_t, std::vector<CXCursor_int_t>>>
CODEAI_EXPORT get_path_to_lineno_to_nodes(pointer_container_t tu_val, std::string match_pattern, std::string path){
    bool need_match = false;
    std::regex pattern;
    if (match_pattern != ""){
        need_match = true;
        pattern = std::regex(match_pattern);
    }
    std::unordered_map<std::string, std::unordered_map<int64_t, std::vector<CXCursor_int_t>>> res;
    CXTranslationUnit tu = reinterpret_cast<CXTranslationUnit>(tu_val);
    if (!tu){
        return res;
    }

    auto cu = clang_getTranslationUnitCursor(tu);
    auto init_childs = get_cursor_children(cu);
    std::deque<CXCursor> q(init_childs.begin(), init_childs.end());
    std::unordered_set<std::string> ignored;
    while (!q.empty()){
        CXCursor cur_node = q.back();
        q.pop_back();
        CXSourceLocation loc = clang_getCursorLocation(cur_node);
        CXFile f;
        uint32_t line, column, offset;
        clang_getInstantiationLocation(loc, &f, &line, &column, &offset);
        if (!f){
            continue;
        }
        auto cxname = clang_getFileName(f);
        std::string filepath = clang_getCString(cxname); 
        clang_disposeString(cxname);
        if (ignored.find(filepath) != ignored.end()){
            continue;
        }
        if (path != filepath){
            if (!need_match || !std::regex_match(filepath, pattern)){
                ignored.insert(filepath);
                continue;
            }
        }
        CXCursor_int_t cursor_int_res;
        std::get<0>(cursor_int_res) = cur_node.kind;
        std::get<1>(cursor_int_res) = cur_node.xdata;
        auto& cur_datas = std::get<2>(cursor_int_res);
        cur_datas[0] = reinterpret_cast<std::uintptr_t>(cur_node.data[0]);
        cur_datas[1] = reinterpret_cast<std::uintptr_t>(cur_node.data[1]);
        cur_datas[2] = reinterpret_cast<std::uintptr_t>(cur_node.data[2]);

        res[filepath][line].push_back(cursor_int_res);
        auto next_childs = get_cursor_children(cur_node);
        for (auto it = next_childs.rbegin(); it != next_childs.rend(); ++it){
            q.push_back(*it);
        }
    }
    return res;
}

std::unordered_map<std::string, std::unordered_map<int64_t, std::vector<CXCursor_int_t>>>
CODEAI_EXPORT update_path_lineno(CXCursor_int_t cu_val, std::string match_pattern, std::string path){
    bool need_match = false;
    std::regex pattern;
    if (match_pattern != ""){
        need_match = true;
        pattern = std::regex(match_pattern);
    }
    std::unordered_map<std::string, std::unordered_map<int64_t, std::vector<CXCursor_int_t>>> res;
    CXCursor cu;
    cu.kind = CXCursorKind(std::get<0>(cu_val));
    cu.xdata = std::get<1>(cu_val);
    auto ptr_vals =  std::get<2>(cu_val);
    cu.data[0] = reinterpret_cast<const void*>(ptr_vals[0]);
    cu.data[1] = reinterpret_cast<const void*>(ptr_vals[1]);
    cu.data[2] = reinterpret_cast<const void*>(ptr_vals[2]);
    std::deque<CXCursor> q;
    q.push_back(cu);
    std::unordered_set<std::string> ignored;

    while (!q.empty()){
        CXCursor cur_node = q.back();
        q.pop_back();
        CXSourceLocation loc = clang_getCursorLocation(cur_node);
        CXFile f;
        uint32_t line, column, offset;
        clang_getInstantiationLocation(loc, &f, &line, &column, &offset);
        if (!f){
            continue;
        }
        auto cxname = clang_getFileName(f);
        std::string filepath = clang_getCString(cxname); 
        clang_disposeString(cxname);
        if (ignored.find(filepath) != ignored.end()){
            continue;
        }
        if (path != filepath){
            if (!need_match || !std::regex_match(filepath, pattern)){
                ignored.insert(filepath);
                continue;
            }
        }
        CXCursor_int_t cursor_int_res;
        std::get<0>(cursor_int_res) = cur_node.kind;
        std::get<1>(cursor_int_res) = cur_node.xdata;
        auto& cur_datas = std::get<2>(cursor_int_res);
        cur_datas[0] = reinterpret_cast<std::uintptr_t>(cur_node.data[0]);
        cur_datas[1] = reinterpret_cast<std::uintptr_t>(cur_node.data[1]);
        cur_datas[2] = reinterpret_cast<std::uintptr_t>(cur_node.data[2]);
        res[filepath][line].push_back(cursor_int_res);
        auto next_childs = get_cursor_children(cur_node);
        for (auto it = next_childs.rbegin(); it != next_childs.rend(); ++it){
            q.push_back(*it);
        }
    }
    return res;

}

std::unordered_map<std::string, std::vector<CXCursor_int_t>>
CODEAI_EXPORT get_path_to_nodes(CXCursor_int_t cu_val, std::string match_pattern, std::string path){
    bool need_match = false;
    std::regex pattern;
    if (match_pattern != ""){
        need_match = true;
        pattern = std::regex(match_pattern);
    }
    std::unordered_map<std::string, std::vector<CXCursor_int_t>> res;
    CXCursor cu;
    cu.kind = CXCursorKind(std::get<0>(cu_val));
    cu.xdata = std::get<1>(cu_val);
    auto ptr_vals =  std::get<2>(cu_val);
    cu.data[0] = reinterpret_cast<const void*>(ptr_vals[0]);
    cu.data[1] = reinterpret_cast<const void*>(ptr_vals[1]);
    cu.data[2] = reinterpret_cast<const void*>(ptr_vals[2]);
    auto init_childs = get_cursor_children(cu);
    std::vector<CXCursor> q(init_childs.begin(), init_childs.end());
    std::unordered_set<std::string> ignored;
    for (auto& cur_node : init_childs){
        CXSourceLocation loc = clang_getCursorLocation(cur_node);
        CXFile f;
        uint32_t line, column, offset;
        clang_getInstantiationLocation(loc, &f, &line, &column, &offset);
        if (!f){
            continue;
        }
        auto cxname = clang_getFileName(f);
        std::string filepath = clang_getCString(cxname); 
        clang_disposeString(cxname);
        if (ignored.find(filepath) != ignored.end()){
            continue;
        }
        if (path != filepath){
            if (!need_match || !std::regex_match(filepath, pattern)){
                ignored.insert(filepath);
                continue;
            }
        }
        CXCursor_int_t cursor_int_res;
        std::get<0>(cursor_int_res) = cur_node.kind;
        std::get<1>(cursor_int_res) = cur_node.xdata;
        auto& cur_datas = std::get<2>(cursor_int_res);
        cur_datas[0] = reinterpret_cast<std::uintptr_t>(cur_node.data[0]);
        cur_datas[1] = reinterpret_cast<std::uintptr_t>(cur_node.data[1]);
        cur_datas[2] = reinterpret_cast<std::uintptr_t>(cur_node.data[2]);
        res[filepath].push_back(cursor_int_res);
    }
    return res;
}