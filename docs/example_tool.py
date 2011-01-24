class MultiplyTool(object):
    def run(self, input_vars, **kwargs):
    
        x = input_vars['x']
        y = input_vars['y']
        
        z = x * y
        
        result = {'z': z}
        
        return result
        
