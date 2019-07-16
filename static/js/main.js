$(document).ready(function() {
    $('#login-form').form({
        fields: {
            email: {
                identifier: 'email',
                rules: [{
                        type: 'empty',
                        prompt: 'Please enter your e-mail'
                    },
                    {
                        type: 'email',
                        prompt: 'Please enter a valid e-mail'
                    }
                ]
            },
            password: {
                identifier: 'password',
                rules: [{
                        type: 'empty',
                        prompt: 'Please enter your password'
                    },
                    {
                        type: 'length[6]',
                        prompt: 'Your password must be at least 6 characters'
                    }
                ]
            }
        }
    });

    $('#reg-form').form({
        fields: {
            name: {
                identifier: 'name',
                rules: [{
                    type: 'empty',
                    prompt: 'Please enter your name'
                }, ]
            },
            surname: {
                identifier: 'surname',
                rules: [{
                    type: 'empty',
                    prompt: 'Please enter your surname'
                }, ]
            },
            email: {
                identifier: 'email',
                rules: [{
                        type: 'empty',
                        prompt: 'Please enter your e-mail'
                    },
                    {
                        type: 'email',
                        prompt: 'Please enter a valid e-mail'
                    }
                ]
            },
            password: {
                identifier: 'password',
                rules: [{
                        type: 'empty',
                        prompt: 'Please enter your password'
                    },
                    {
                        type: 'length[6]',
                        prompt: 'Your password must be at least 6 characters'
                    }
                ]
            },
            confirmation: {
                identifier: 'confirmation',
                rules: [{
                        type: 'empty',
                        prompt: 'Please repeat your password'
                    },
                    {
                        type: 'length[6]',
                        prompt: 'Your password must be at least 6 characters'
                    }
                ]
            }
        }
    });
});