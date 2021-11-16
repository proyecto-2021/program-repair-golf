require 'minitest/autorun'
require_relative 'example22'

class MedianTest < Minitest::Test
  def test_1
    assert median(1,2,3) == 2
  end

  def test_2
    assert median(2,1,3) == 2
  end

  def test_3
    assert median(3,1,2) == 2
  end
end
