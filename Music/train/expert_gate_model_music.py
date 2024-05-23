from keras import regularizers
from keras.layers import Dropout, Attention, MultiHeadAttention, LeakyReLU, ELU, PReLU
from keras.layers import Input, Dense
import tensorflow as tf
from keras import backend as K
from keras.layers import Input, Dense
from keras.models import Model


attention = Attention()
# 定义子模型
def expert_model(input_shape):
    inputs = Input(shape=input_shape)
    x = Dense(128, activation='relu')(inputs)
    outputs = Dense(16, activation='relu')(x)
    model = Model(inputs=inputs, outputs=outputs)
    return model

# 定义门网络
def gate_model(input_shape, num_experts):
    inputs = Input(shape=input_shape)
    x = Dense(44, activation='relu')(inputs)
    x = K.expand_dims(x, axis=1)
    x = Attention()([x, x])
    outputs = Dense(num_experts, activation='relu')(x)
    print(outputs)
    outputs = K.repeat_elements(outputs, 16, axis=1)
    model = Model(inputs=inputs, outputs=outputs)
    return model

# 定义共享模型 只输出专家输出的结果
def ShareMoE(input_shape, num_experts):
    inputs = Input(shape=input_shape)
    experts_outputs = []
    for i in range(num_experts):
        expert_inputs = inputs
        expert = expert_model(input_shape)(expert_inputs)
        expert = K.expand_dims(expert, axis=0)
        experts_outputs.append(expert)
    output = tf.concat(experts_outputs, axis=0)
    output = tf.transpose(output, [1, 2, 0])
    model = Model(inputs=inputs, outputs=output)
    return model

# 定义tower与output层
def tower_output(input_shape):
    inputs = Input(shape=input_shape)
    x = Dense(input_shape, activation='linear')(inputs)
    output = Dense(10, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=output)
    return model

# 门网络对共享网络输出进行加权处理
def multiply(output1, output2):
    output = tf.multiply(output1, output2)
    output = K.sum(output, axis=2)
    return output

