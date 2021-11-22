const median = require('./median')

test('test1', () => {
	expect(median(1,2,3)).toBe(2);
});

test('test2', () => {
	expect(median(2,1,3)).toBe(2);
});

test('test3', () => {
	expect(median(3,1,2)).toBe(2);
});

