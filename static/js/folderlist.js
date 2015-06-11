var selected = null;

function init(rawList, parent) {
	var result = [];
	rawList.forEach(function(element) {
			console.log(element)
			element.parent = parent;
		if (element.children) {
			element.children = init(element.children, element.id);
		}
		result.push(element);
	}, this);
	return result;
}