
<!--
## Original Input: -2*(3+5)+7


## After Tokinizer:
tokens =
    [
        { tag: "-", value: "-"},
        { tag: "number", value: 2 },
        { tag: "*", value: "*" },
        { tag: "(", value: "(" },
        { tag: "number", value: 3 },
        { tag: "+", value: "+" },
        { tag: "number", value: 5 },
        { tag: ")", value: ")" },
        { tag: "+", value: "+" },
        { tag: "number", value: 7 }
    ]

## After parser

//expression tree
parserOutput =
{
    tag: "+",
    left: {
        tag: "*",
        left: { //-2
            tag: "negative",
            value: {
                tag: "number", value: "2"
            }
        },
        right: { //res of (3+5)
            tag: "+",
            left: { tag: "number", value: "3" },
            right: { tag: "number", value: "5" }
        }
    },
    right: {tag: "number", value: "7"}
}
-->