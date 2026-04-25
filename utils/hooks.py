
activation_cache = {
    'encoder': {
        'layer_name': None,
        'eval_vectors': None
    },
    'decoder': {
        'layer_name': None,
        'eval_vectors': None
    }
}


def get_activation(stage, layer_name):
    def hook(model, input, output):
        if isinstance(output, tuple):
            tensor_out = output[0]
        else:
            tensor_out = output
            
        activation_cache[stage]['eval_vectors'] = tensor_out.detach().cpu().numpy()
        activation_cache[stage]['layer_name'] = layer_name
        
    return hook


model.encoder_layers[-1].register_forward_hook(
    get_activation('encoder', 'encoder_layer_final')
)


model.decoder_layers[0].register_forward_hook(
    get_activation('decoder', 'decoder_layer_0')
)

