require 'minitest/autorun'
require_relative 'fibonacci'

class FibonacciTest < Minitest::Test
  def test_1
    assert fibonacci(0) == 1
  end

  def test_2
    assert fibonacci(1) == 1
  end

  def test_3
    assert fibonacci(2) == 3      
  end

  def test_4
    assert fibonacci(8) == 34
  end
end