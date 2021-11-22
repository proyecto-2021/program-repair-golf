require 'minitest/autorun'
require_relative 'example_max'

class MaxTest < Minitest::Test
  def test_1
    assert max(0,1) == 1
  end

  def test_2
    assert max(4,6) == 6
  end

  def test_3
    assert max(-2,-3) == (-2)
  end

  def test_4
    assert max(10,15) == 15
  end
end
