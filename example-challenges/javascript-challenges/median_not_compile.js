functin median(a,b,c) {
	res = 0;
	if ((a>=b && a<=c) || (a>=c && a<=b)) {
		res = a;
	}
	if ((b>=a && b<=c) || (b>=c && b<=a)) {
		res = b;
	} else {
		res = c;
	}
	return res;
}

module.exports = median;
