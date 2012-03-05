function CanvasLite(x, y, w, h, p) {
    this.addToParent = function() {
        if (p) {
            p._AddChild(this);
        }
    }
    this.removeFromParent = function() {
        if (p) {
            p._RemoveChild(this);
        }
    }
    this.addToParent();
    var canvas = document.createElement('canvas');
    document.body.appendChild(canvas);

    var children = new Array();

    this._AddChild = function(child) {
        children.push(child);
    };

    this._RemoveChild = function(child) {
        for (i = 0; i < children.length; ++i) {
            if (children[i] == child) {
                children.splice(i, 1);
                return;
            }
        }
    };

    this.del = function() {
        document.body.removeChild(canvas);
        this.removeFromParent()
        for (i in children) {
            children[i].del();
        }
    };

    var referX = 0;
    var referY = 0;

    this.reset = function() {
        this.del();
        document.body.appendChild(canvas);
        this.addToParent();
        canvas.style.left = x + referX;
        canvas.style.top = y + referY;
    };

    var z = 0;
    if (p) {
        referX = p._AbsX();
        referY = p._AbsY();
        z = p.z() + 1;
    }
    canvas.style.left = x + referX;
    canvas.style.top = y + referY;
    canvas.style.zIndex = z;
    canvas.style.position = 'absolute';
    canvas.width = w;
    canvas.height = h;

    this.z = function() {
        return z;
    };
    this._AbsX = function() {
        if (p) {
            return x + p._AbsX();
        }
        return x;
    };
    this._AbsY = function() {
        if (p) {
            return y + p._AbsY();
        }
        return y;
    };

    var ctxt = canvas.getContext('2d');
    this.context = function() {
        return ctxt;
    };

    this.show = function() {
        canvas.style.visibility = 'visible';
        for (i in children) {
            children[i].show();
        }
    };

    this.hide = function() {
        canvas.style.visibility = 'hidden';
        for (i in children) {
            children[i].hide();
        }
    };

    function packFunc(f) {
        return function(event) {
            f(event.offsetX, event.offsetY);
        };
    }

    this.hover = function(f) {
        canvas.onmouseover = packFunc(f);
    };

    this.click = function(f) {
        canvas.onclick = packFunc(f);
    };

    this.paintBorder = function(color, borderSize) {
        ctxt.save();
        ctxt.fillStyle = color;
        ctxt.fillRect(0, 0, w, borderSize);
        ctxt.fillRect(0, 0, borderSize, h);
        ctxt.fillRect(0, h - borderSize, w, borderSize);
        ctxt.fillRect(w - borderSize, 0, borderSize, h);
        ctxt.restore();
    };

    this.fillBg = function(color) {
        ctxt.save();
        ctxt.fillStyle = color;
        ctxt.fillRect(0, 0, w, h);
        ctxt.restore();
    };
}
