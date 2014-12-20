/**
 * Created by bqh on 12/8/14.
 */
$(jq_Controls());

function jq_Controls(){

    $.each($('.check-btn>input:checked'), function(){
        this.parent().addClass('active');
    });

}