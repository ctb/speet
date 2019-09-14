from speet import ScaledMinHash


def test_similarity_1():
    m1 = ScaledMinHash(scaled=1)
    m2 = ScaledMinHash(scaled=1)

    assert m1.similarity(m2) == 0
    assert m1.contained_by(m2) == 0
    assert m2.contained_by(m1) == 0

    m1.add_text("hello world")
    m2.add_text("hello world")
    assert m1.similarity(m2) == 1.0


def test_similarity_2():
    m1 = ScaledMinHash(scaled=1)
    m2 = ScaledMinHash(scaled=1)

    m1.add_text("hello")
    m2.add_text("hello")
    m1.add_text("world")
    m2.add_text("fools")

    assert m1.similarity(m2) == 1/3
