const median = require('./example_not_exist.js')

test('test1', () => {
	expect(median(1,2,3)).toBe(2);
});

test('test3', () => {
	expect(median(3,1,2)).toBe(2);
});

