require 'minitest/autorun'
require_relative 'example_put5'

class MedianTest < Minitest::Test
  def test_1
    assert median2(1,2,3) == 2
  end

  def test_2
    assert median2(2,1,3) == 2
  end

  def test_3
    assert median2(3,1,2) == 2
  end
end
