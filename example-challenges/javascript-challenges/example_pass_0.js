function median(a,b,c) {
	res = 0;
	if ((a>=b && a<=c) || (a>=c && a<=b)) {
		res = a;
	}
	else if ((b>=a && b<=c) || (b>=c && b<=a)) {
		res = b;
	} else {
		res = c;
	}
	return res;
}

module.exports = median;
