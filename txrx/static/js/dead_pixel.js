window.onload = function() {
  function getCookie(c_name) {
    if (document.cookie.length > 0) {
      c_start = document.cookie.indexOf(c_name + "=");
      if (c_start != -1) {
	c_start = c_start + c_name.length + 1;
	c_end = document.cookie.indexOf(";", c_start);
	if (c_end == -1) {
          c_end = document.cookie.length;
	}
	return unescape(document.cookie.substring(c_start, c_end));
      }
    }
    return "";
  }
  function deadPixel(top,left,color) {
    if (top==undefined) { top = Math.floor(Math.random()*100) }
    if (left==undefined) { left = Math.floor(Math.random()*100) }
    if (color==undefined) { color = ["#F00","#0F0","#00F","#000"][Math.floor(Math.random()*4)] }
    var p = document.createElement('div');
    p.style.position = "fixed";
    p.style.zIndex = "2147483647";
    p.style.top = top+"%";
    p.style.left = left+"%";
    p.style.backgroundColor = color;
    p.className = "deadPixel";
    p.style.width = "1px";
    p.style.height = "1px";
    document.body.appendChild(p);
    return [top,left,color].join(',')
  }
  var pixel_str = getCookie("arstneiojkrofl");
  var pixels = pixel_str.split('|');
  for (var i=0;i<pixels.length; i++) {
    var p = pixels[i].split(',');
    if (p.length !=3) { continue }
    var top = p[0], left = p[1], color = p[2];
    deadPixel(top,left,color);
  }
  if (pixels.length < 2 || Math.random() > 0.5) { pixels.push(deadPixel()) }
  document.cookie = name + "arstneiojkrofl=" + pixels.join("|") +";path=/";
}