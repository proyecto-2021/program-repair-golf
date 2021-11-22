require 'minitest/autorun'
require_relative 'addition'

class AdditionTest < Minitest::Test
  def test_1
    assert addition(1,2) == 3
  end

  def test_2
    assert addition(1,3) == 4
  end

  def test_3
    assert addition(3,2) == 5
  end
end
