$(document).ready(function () {
    $('input[type="checkbox"]').each(function () {
        var $checkbox = $(this);
        var $btn = $checkbox.closest('.btn');

        if ($checkbox.is(':checked')) {
            $btn.addClass('active');
        }

        $checkbox.change(function () {
            if ($checkbox.is(':checked')) {
                $btn.addClass('active');
            } else {
                $btn.removeClass('active');
            }
        });
    });
});