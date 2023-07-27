import math

headerId_counter = 0
orderId_counter = 0
static_direction = [
    (3.14159265358979323846 / 180 * 0),
    (3.14159265358979323846 / 180 * 90),
    (3.14159265358979323846 / 180 * 180),
    (3.14159265358979323846 / 180 * 270),
    -(3.14159265358979323846 / 180 * 90),
    -(3.14159265358979323846 / 180 * 180),
    -(3.14159265358979323846 / 180 * 270),
]

def find_nearest_dir(value, direction_list):
    return min(direction_list, key=lambda x: abs(x - value))


def create_update_turn_dict(current_position, new_nearest_node, direction):
    global headerId_counter, orderId_counter
    
    nodes = []
    edges = []
    for i, pos in enumerate([current_position] + [current_position]):
        node_id = "nodeId" + str(i * 2)
        sequence_id = i * 2
        if i == 0:
          nodes.append({
              "nodeId": node_id,
              "sequenceId": sequence_id,
              "nodePosition": {"x": new_nearest_node['x'], "y": new_nearest_node['y'], "theta": pos['theta']},
              "actions": []
          })
        if i != 0:
            nodes.append({
              "nodeId": node_id,
              "sequenceId": sequence_id,
              "nodePosition": {"x": new_nearest_node['x'], "y": new_nearest_node['y'], "theta": (3.14159265358979323846 / 180 * direction)},
              "actions": []
            })
            edge_id = sequence_id = (sequence_id + (i - 1) * 2) // 2
            edges.append({
                "edgeId": str(edge_id),
                "sequenceId": sequence_id,
                "maxSpeed": 1,
                "maxAcceleration": 1,
                "maxDeceleration": 1,
                "startNodeId": "nodeId" + str((i - 1) * 2),
                "endNodeId": node_id,
                "avoidance": True
            })
    
    turn = {
        "headerId": headerId_counter,
        "timestamp": "",
        "version": "",
        "manufacturer": "",
        "serialNumber": "NO.048",
        "orderId": str(orderId_counter),
        "orderUpdateId": 0,
        "nodes": nodes,
        "edges": edges
    }
    
    # Increase headerId and orderId counters
    headerId_counter += 1
    orderId_counter += 1
    
    return turn

def create_update_forward_dict(current_position, new_nearest_node, target_positions):
    global headerId_counter, orderId_counter
    
    # Create and fill nodes and edges
    nodes = []
    edges = []
    for i, pos in enumerate([current_position] + [target_positions]):
        node_id = "nodeId" + str(i * 2)
        sequence_id = i * 2
        if i == 0:
          nodes.append({
              "nodeId": node_id,
              "sequenceId": sequence_id,
              "nodePosition": {"x": new_nearest_node['x'], "y": new_nearest_node['y'], "theta": find_nearest_dir(current_position['theta'], static_direction)},
              "actions": []
          })
        if i != 0:
            nodes.append({
              "nodeId": node_id,
              "sequenceId": sequence_id,
              "nodePosition": {"x": target_positions['x'], "y": target_positions['y'], "theta": find_nearest_dir(current_position['theta'], static_direction)},
              "actions": []
            })
            edge_id = sequence_id = (sequence_id + (i - 1) * 2) // 2
            edges.append({
                "edgeId": str(edge_id),
                "sequenceId": sequence_id,
                "maxSpeed": 1,
                "maxAcceleration": 1,
                "maxDeceleration": 1,
                "startNodeId": "nodeId" + str((i - 1) * 2),
                "endNodeId": node_id,
                "avoidance": True
            })
    
    # Create and fill foward dictionary
    foward = {
        "headerId": headerId_counter,
        "timestamp": "",
        "version": "",
        "manufacturer": "",
        "serialNumber": "NO.048",
        "orderId": str(orderId_counter),
        "orderUpdateId": 0,
        "nodes": nodes,
        "edges": edges
    }
    
    # Increase headerId and orderId counters
    headerId_counter += 1
    orderId_counter += 1
    
    return foward

def create_update_angle_dict(current_position, new_nearest_node, angle):
    global headerId_counter, orderId_counter
    nodes = []
    edges = []
    for i, pos in enumerate([current_position] + [current_position]):
        node_id = "nodeId" + str(i * 2)
        sequence_id = i * 2
        if i == 0:
          nodes.append({
              "nodeId": node_id,
              "sequenceId": sequence_id,
              "nodePosition": {"x": new_nearest_node['x'], "y": new_nearest_node['y'], "theta": find_nearest_dir(current_position['theta'], static_direction)},
              "actions": [                {
                "actionType": "tilt",
                "actionId": str(sequence_id),
                "blockingType": "HARD",
                "actionParameters": [
                    {
                        "key": "angle",
                        "value": angle
                    }
                ]
            }]
          })
    
    tilt = {
        "headerId": headerId_counter,
        "timestamp": "",
        "version": "",
        "manufacturer": "",
        "serialNumber": "NO.048",
        "orderId": str(orderId_counter),
        "orderUpdateId": 0,
        "nodes": nodes,
        "edges": edges
    }
    
    # Increase headerId and orderId counters
    headerId_counter += 1
    orderId_counter += 1
    
    return tilt