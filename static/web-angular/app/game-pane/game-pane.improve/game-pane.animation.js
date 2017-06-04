/**
 * Created by jsz on 2016/10/22.
 */
angular.module('gamePaneImprove').
    animation('.gamePaneAni',function gamePaneAniFactory() {
        return {
            addClass: playerArrive,
            removeClass: playerLeave
        };
        function playerArrive(element,className,done) {
            if (className !== 'selected') return;

                element.css({
                    display: 'block',
                    position: 'absolute',
                    top: 500,
                    left: 0
                }).animate({
                    top: 0
                }, done);

            return function animateInEnd(wasCanceled) {
                if (wasCanceled) element.stop();
            };
        }
    });