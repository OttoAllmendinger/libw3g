/*
 * see http://en.wikipedia.org/wiki/HSL_and_HSV#Conversion_from_HSL_to_RGB
 */


jQuery.fn.autocontrast = function(background) {
    $(this).css('color', $.autocontrast($(this).text(), background));
}

jQuery.autocontrast = function(text, background) {
    var hash01 = function(text) {
        return Math.abs(crc32(text) % 512)/512;
    }

    if (background=="dark") {
        var h = hash01(text+'_h'),
            s = 0.1 + 0.9 * hash01(text+'_s'),
            l = 0.4 + 0.2 * hash01(text+'_v');
    } else {
        var h = hash01(text+'h'),
            s = 0.4 + 0.6 * hash01(text+'s'),
            l = 0.0 + 0.3 * hash01(text+'v');
    }

    return $.RGB(hslToRgb(h,s,l));
}



jQuery.autocontrast_test = function(canvas) {
    var context = canvas.getContext('2d'),
        W = canvas.width,
        H = canvas.height,
        newPixels = context.createImageData(W, H),
        pix = newPixels.data;
        setRGB = function (x, y, r, g, b) {
            var i = 4*(y*W+x);
            pix[i] = r;
            pix[i+1] = g;
            pix[i+2] = b;
            pix[i+3] = 255;
        };

    for (var i=0; i<255; i+=1) {
        for (var j=0; j<255; j++) {
            var color = hslToRgb(i/255.0, 1.0, 0.7);
            setRGB(i, j, color[0], color[1], color[2]);
        }
    }

    console.log($(this).hash);

    context.putImageData(newPixels, 0, 0);
}
