require 'minitest/autorun'
require_relative 'example_factorial'

class FactorialTest < Minitest::Test
  def test_1
    assert factorial(0) == 1
  end

  def test_2
    assert factorial(1) == 1
  end

  def test_3
    assert factorial(3) == 6
  end

  def test_4
    assert factorial(10) == 3628800
  end
end
