from elem import Elem, Text
from elements import Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br

class Page:
    """
    Class Page.
    This class validates and represents an HTML page.
    """

    ALLOWED_TAGS = {Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text}
    
    def __init__(self, elem: Elem) -> None:
        if not isinstance(elem, Elem):
            raise Elem.ValidationError()
        self.elem = elem
        self.elem = elem
    
    def __str__(self) -> str:
        res = "<!DOCTYPE html>\n" + str(self.elem)
        return res
    
    def write_to_file(self, filename: str) -> None:
        """Writes the HTML content to a file."""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(self))
    
    def is_valid(self) -> bool:
        """Validates the HTML tree structure."""
        return self._validate_node(self.elem)
    
    def _validate_node(self, node: Elem) -> bool:
        if not isinstance(node,  tuple(self.ALLOWED_TAGS)):
            return False

        children = node.content if isinstance(node.content, list) else [node.content] if node.content else []
        children = [child for child in children if child is not None]

        if isinstance(node, Html):
            return len(children) == 2 and isinstance(children[0], Head) and isinstance(children[1], Body)
        
        if isinstance(node, Head):
            titles = [child for child in children if isinstance(child, Title)]
            return len(titles) == 1 and all(isinstance(child, (Title, Meta)) for child in children)
        
        if isinstance(node, Body) or isinstance(node, Div):
            return all(isinstance(child, (H1, H2, Div, Table, Ul, Ol, Span, Text)) for child in children)
        
        if isinstance(node, (Title, H1, H2, Li, Th, Td)):
            return len(children) == 1 and isinstance(children[0], Text)
        
        if isinstance(node, P):
            return all(isinstance(child, Text) for child in children)
        
        if isinstance(node, Span):
            return all(isinstance(child, (Text, P)) for child in children)
        
        if isinstance(node, (Ul, Ol)):
            return len(children) > 0 and all(isinstance(child, Li) for child in children)
        
        if isinstance(node, Tr):
            ths = [child for child in children if isinstance(child, Th)]
            tds = [child for child in children if isinstance(child, Td)]
            return (len(ths) > 0 and len(tds) == 0) or (len(tds) > 0 and len(ths) == 0)
        
        if isinstance(node, Table):
            return all(isinstance(child, Tr) for child in children)
        
        return True


def __print_test(target: Page, toBe: bool):
    print("================START===============")
    print(str(target))
    print("===============IS_VALID=============")
    # print( target.is_valid() == toBe)
    
    print("{:^36s}".format(str(toBe)))
    print("{:^36s}".format(str(target.is_valid())))
    print("=================END================")


def __test_Table():
    print("\n%{:=^34s}%\n".format("Table"))
    target = Page(Table())
    __print_test(target, True)
    target = Page(
        Table(
            [
                Tr(),
            ]))
    __print_test(target, True)
    target = Page(
        Table(
            [
                H1(
                    Text("Hello World!")
                ),
            ]))
    __print_test(target, False)


def __test_Tr():
    print("\n%{:=^34s}%\n".format("Tr"))
    target = Page(Tr())
    __print_test(target, False)
    target = Page(
        Tr(
            [
                Th(Text("title")),
                Th(Text("title")),
                Th(Text("title")),
                Th(Text("title")),
                Th(Text("title")),
            ]))
    __print_test(target, True)
    target = Page(
        Tr(
            [
                Td(Text("content")),
                Td(Text("content")),
                Td(Text("content")),
                Td(Text("content")),
                Td(Text("content")),
                Td(Text("content")),
            ]))
    __print_test(target, True)
    target = Page(
        Tr(
            [
                Th(Text("title")),
                Td(Text("content")),
            ]))
    __print_test(target, False)


def __test_Ul_OL():
    print("\n%{:=^34s}%\n".format("Ul_OL"))
    target = Page(
        Ul()
    )
    __print_test(target, False)
    target = Page(
        Ol()
    )
    __print_test(target, False)
    target = Page(
        Ul(
            Li(
                Text('test')
            )
        )
    )
    __print_test(target, True)
    target = Page(
        Ol(
            Li(
                Text('test')
            )
        )
    )
    __print_test(target, True)
    target = Page(
        Ul([
            Li(
                Text('test')
            ),
            Li(
                Text('test')
            ),
        ])
    )
    __print_test(target, True)
    target = Page(
        Ol([
            Li(
                Text('test')
            ),
            Li(
                Text('test')
            ),
        ])
    )
    __print_test(target, True)
    target = Page(
        Ul([
            Li(
                Text('test')
            ),
            H1(
                Text('test')
            ),
        ])
    )
    __print_test(target, False)
    target = Page(
        Ol([
            Li(
                Text('test')
            ),
            H1(
                Text('test')
            ),
        ])
    )
    __print_test(target, False)


def __test_Span():
    print("\n%{:=^34s}%\n".format("Span"))
    target = Page(
        Span()
    )
    __print_test(target, True)
    target = Page(
        Span([
            Text("Hello?"),
            P(Text("World!")),
        ])
    )
    __print_test(target, True)
    target = Page(
        Span([
            H1(Text("World!")),
        ])
    )
    __print_test(target, False)


def __test_P():
    print("\n%{:=^34s}%\n".format("P"))
    target = Page(
        P()
    )
    __print_test(target, True)
    target = Page(
        P([
            Text("Hello?"),
        ])
    )
    __print_test(target, True)
    target = Page(
        P([
            H1(Text("World!")),
        ])
    )
    __print_test(target, False)


def __test_Title_H1_H2_Li_Th_Td():
    print("\n%{:=^34s}%\n".format("H1_H2_Li_Th_Td"))
    for c in [H1, H2, Li, Th, Td]:
        target = Page(
            c()
        )
        __print_test(target, False)
        target = Page(
            c([
                Text("Hello?"),
            ])
        )
        __print_test(target, True)
        target = Page(
            c([
                H1(Text("World!")),
            ])
        )
        __print_test(target, False)
        target = Page(
            c([
                Text("Hello?"),
                Text("Hello?"),
            ])
        )
        __print_test(target, False)


def __test_Body_Div():
    print("\n%{:=^34s}%\n".format("Body_Div"))
    for c in [Body, Div]:
        target = Page(
            c()
        )
        __print_test(target, True)
        target = Page(
            c([
                Text("Hello?"),
            ])
        )
        __print_test(target, True)
        target = Page(
            c([
                H1(Text("World!")),
            ])
        )
        __print_test(target, True)
        target = Page(
            c([
                Text("Hello?"),
                Span(),
            ])
        )
        __print_test(target, True)
        target = Page(
            c([
                Html(),
                c()
            ])
        )
        __print_test(target, False)


def __test_Title():
    print("\n%{:=^34s}%\n".format("Title"))
    target = Page(
        Title()
    )
    __print_test(target, False)
    target = Page(
        Title([
            Title(Text("Hello?")),
        ])
    )
    __print_test(target, True)
    target = Page(
        Title([
            Title(Text("Hello?")),
            Title(Text("Hello?")),
        ])
    )
    __print_test(target, False)


def __test_Html():
    print("\n%{:=^34s}%\n".format("Html"))
    target = Page(
        Html()
    )
    __print_test(target, False)
    target = Page(
        Html([
            Head([
                Title(Text("Hello?")),
            ]),
            Body([
                H1(Text("Hello?")),
            ])
        ])
    )
    __print_test(target, True)
    target = Page(
        Html(
            Div()
        )
    )
    __print_test(target, False)


def __test_Elem():
    __print_test(Page(Elem()), False)


def __test_write_to_file(target: Page, path: str):
    print("================START===============")
    print(str(target))
    print("==========WRITE_TO_FILE=============")
    target.write_to_file(path)
    print("{:^36s}".format(path))
    print("=================END================")


def __test():
    __test_Table()
    __test_Tr()
    __test_Ul_OL()
    __test_Span()
    __test_P()
    __test_Title_H1_H2_Li_Th_Td()
    __test_Body_Div()
    __test_Html()
    __test_Elem()
    __test_write_to_file(
        Page(Html([Head(Title(Text("hello world!"))),
             Body(H1(Text("HELLO WORLD!")))])),
        "__test_write_to_file.html")


if __name__ == '__main__':
    __test()