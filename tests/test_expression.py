from unittest.mock import ANY

from hassil.expression import (
    Group,
    GroupType,
    ListReference,
    RuleReference,
    Sentence,
    TextChunk,
)
from hassil.parse_expression import parse_expression, parse_sentence
from hassil.parser import next_chunk

# -----------------------------------------------------------------------------


def test_word():
    assert parse_expression(next_chunk("test")) == t(text="test")


def test_group_in_group():
    assert parse_expression(next_chunk("((test test2))")) == sequence(
        items=[sequence(items=[t(text="test "), t(text="test2")])],
    )


def test_escapes():
    assert parse_expression(next_chunk(r"(test\<\>\{\}\)\( test2)")) == sequence(
        items=[t(text="test<>{})( "), t(text="test2")],
    )


def test_optional():
    assert parse_expression(next_chunk("[test test2]")) == alt(
        items=[
            sequence(
                items=[t(text="test "), t(text="test2")],
            ),
            t(text=""),
        ],
        is_optional=True,
    )


def test_group_alternative():
    assert parse_expression(next_chunk("(test | test2)")) == alt(
        items=[sequence(items=[t(text="test ")]), sequence(items=[t(text=" test2")])],
    )


def test_group_permutation():
    assert parse_expression(next_chunk("(test; test2)")) == alt(
        items=[
            sequence(items=[t(text="test"), t(text=" "), t(text=" test2")]),
            sequence(items=[t(text=" test2"), t(text=" "), t(text="test")]),
        ],
    )


def test_slot_reference():
    assert parse_expression(next_chunk("{test}")) == ListReference(list_name="test")


def test_rule_reference():
    assert parse_expression(next_chunk("<test>")) == RuleReference(rule_name="test")


def test_sentence_no_group():
    assert parse_sentence("this is a test") == Sentence(
        items=[t(text="this "), t(text="is "), t(text="a "), t(text="test")]
    )


def test_sentence_group():
    assert parse_sentence("(this is a test)") == Sentence(
        items=[t(text="this "), t(text="is "), t(text="a "), t(text="test")]
    )


def test_sentence_optional():
    assert parse_sentence("[this is a test]") == Sentence(
        type=GroupType.ALTERNATIVE,
        items=[
            sequence(
                items=[
                    t(text="this "),
                    t(text="is "),
                    t(text="a "),
                    t(text="test"),
                ]
            ),
            t(text=""),
        ],
        is_optional=True,
    )


def test_sentence_optional_prefix():
    assert parse_sentence("[t]est") == Sentence(
        type=GroupType.SEQUENCE,
        items=[
            alt(items=[sequence(items=[t(text="t")]), t(text="")], is_optional=True),
            t(text="est"),
        ],
    )


def test_sentence_optional_suffix():
    assert parse_sentence("test[s]") == Sentence(
        type=GroupType.SEQUENCE,
        items=[
            t(text="test"),
            alt(items=[sequence(items=[t(text="s")]), t(text="")], is_optional=True),
        ],
    )


def test_sentence_alternative_whitespace():
    assert parse_sentence("test ( 1 | 2)") == Sentence(
        type=GroupType.SEQUENCE,
        items=[
            t(text="test "),
            alt(
                items=[sequence(items=[t(text=" 1 ")]), sequence(items=[t(text=" 2")])]
            ),
        ],
    )


# def test_fix_pattern_whitespace():
#     assert fix_pattern_whitespace("[start] middle [end]") == "[(start) ]middle[ (end)]"
#     assert fix_pattern_whitespace("start [middle] end") == "start[ (middle)] end"
#     assert fix_pattern_whitespace("start (middle [end])") == "start (middle[ (end)])"
#     assert (
#         fix_pattern_whitespace("[start] (middle) [end]") == "[(start) ](middle)[ (end)]"
#     )


# -----------------------------------------------------------------------------


def t(**kwargs):
    return TextChunk(parent=ANY, **kwargs)


def sequence(**kwargs):
    return Group(type=GroupType.SEQUENCE, **kwargs)


def alt(**kwargs):
    return Group(type=GroupType.ALTERNATIVE, **kwargs)
