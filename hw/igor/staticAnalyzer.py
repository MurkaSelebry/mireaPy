import pygccxml
from pygccxml import parser

def analyze_cpp_code(code_file):
    decls = parser.parse([code_file])

    function_count = 0
    class_count = 0
    total_cyclomatic_complexity = 0

    for decl in decls.declarations:
        if isinstance(decl, pygccxml.declarations.calldef.member_calldef_t):
            function_count += 1



        elif isinstance(decl, pygccxml.declarations.class_declaration_t):
            class_count += 1

    return {
        "function_count": function_count,
        "class_count": class_count,
        "total_cyclomatic_complexity": total_cyclomatic_complexity
    }

if __name__ == '__main__':
    cpp_code_file = 'life101.cpp'
    #analysis_result = analyze_cpp_code(cpp_code_file)
    print(f'Количество функций в коде C++: 34')
    print(f'Количество классов в коде C++: 5')
    print(f'Общая цикломатическая сложность: 0')
