# def cp(num,pic='*',x='x'):
#     box=""
#     for i in range(num):
#         if i==num-1:
#             box+=x
#         else:
#             box+=x
#             box+=pic
#     val=f"({box})"
#     return val

# def xdiff(value,x='x'):
#     box=0
#     for i in value:
#         if i==x:
#             box+=1
        
#     return f'{box}{cp(box-1,x=x)}'
# def xmany(value,x='x'):#논리오류
    
#     idx1=0
#     for i in value[idx1:]:
#         box1=0
#         idx1+=1
#         bb=[]
#         if i=='(':
#             for k in value[idx1:]:
#                 if i==x:
#                     box1+=1
#                 elif i==')':
#                     bb.append(box1)
#                     break
#     val=''
#     for t in bb:
#         val+=f'{t}{cp(t-1,x=x)}'
#     return val
# value=cp(5)+cp(3)+cp(2)
# print(value)
# print(xmany(value))

class PolynomialTerm:
    """
    단항식(예: 4x^3)을 나타내는 클래스입니다.
    계수(coefficient)와 지수(exponent)를 속성으로 가집니다.
    """
    def __init__(self, coefficient, exponent):
        self.coefficient = coefficient
        self.exponent = exponent

    def __str__(self):
        """
        사용자가 요청한 형식(예: 4(x*x*x))으로 객체를 출력합니다.
        """
        if self.coefficient == 0:
            return "0"
        
        # 지수가 0이면 계수만 출력합니다. (예: 2x^0 -> 2)
        if self.exponent == 0:
            return str(self.coefficient)

        # 요청된 형식으로 x의 곱셈을 표현합니다.
        x_mult = '*'.join(['x'] * self.exponent)
        
        # 계수가 1인 경우 생략하여 (x*x*x) 형식으로 출력합니다.
        if self.coefficient == 1:
            return f"({x_mult})"
        else:
            return f"{self.coefficient}({x_mult})"

class XFactory:
    """
    x(3) 또는 x(4,3)과 같은 호출을 가능하게 하는 팩토리 클래스입니다.
    __call__ 메서드를 구현하여 인스턴스를 함수처럼 호출할 수 있습니다.
    """
    def __call__(self, *args):
        if len(args) == 1:
            # 인자가 하나일 경우: x(3) -> 1 * x^3
            return PolynomialTerm(coefficient=1, exponent=args[0])
        elif len(args) == 2:
            # 인자가 두 개일 경우: x(4, 3) -> 4 * x^3
            return PolynomialTerm(coefficient=args[0], exponent=args[1])
        else:
            raise ValueError("인자는 1개 또는 2개여야 합니다.")

# 'x'를 XFactory의 인스턴스로 생성합니다.
x = XFactory()

# ==========================================================
# ✨ 확장된 diff 함수 ✨
# ==========================================================
def diff(*args):
    """
    가변 인자(*args)를 받아 다항식을 미분합니다.
    인자는 PolynomialTerm 객체와 연산자(+, -) 문자열이 번갈아 나타나야 합니다.
    """
    result_parts = []
    
    # 입력된 모든 인자를 하나씩 순회합니다.
    for item in args:
        # 인자가 x()로 생성된 PolynomialTerm 객체인 경우
        if isinstance(item, PolynomialTerm):
            # 미분 공식(d/dx (c * x^n) = c * n * x^(n-1))을 적용합니다.
            new_coefficient = item.coefficient * item.exponent
            new_exponent = item.exponent - 1 if item.exponent > 0 else 0
            
            # 미분된 결과를 새로운 PolynomialTerm 객체로 만듭니다.
            derivative_term = PolynomialTerm(new_coefficient, new_exponent)
            
            # 문자열로 변환하여 결과 리스트에 추가합니다.
            result_parts.append(str(derivative_term))
        
        # 인자가 연산자 문자열인 경우
        elif isinstance(item, str) and item in ['+', '-']:
            # 연산자를 결과 리스트에 그대로 추가합니다.
            result_parts.append(item)
        
        # 지원하지 않는 인자가 들어온 경우 오류를 발생시킵니다.
        else:
            raise TypeError(f"지원하지 않는 인자 타입입니다: {type(item)}")
            
    # 결과 리스트의 모든 요소를 공백으로 연결하여 최종 문자열을 반환합니다.
    return ' '.join(result_parts)

result = diff(x(7,5), '+', x(8,4), '-', x(22,1))
print(result)