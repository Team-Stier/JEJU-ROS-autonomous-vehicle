// Auto-generated. Do not edit!

// (in-package lidar_interfaces.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class ObjectInfo {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.objectCounts = null;
      this.centerX = null;
      this.centerY = null;
      this.centerZ = null;
      this.lengthX = null;
      this.lengthY = null;
      this.lengthZ = null;
      this.minX = null;
      this.minY = null;
      this.minZ = null;
      this.maxX = null;
      this.maxY = null;
      this.maxZ = null;
      this.pixelX = null;
      this.pixelY = null;
    }
    else {
      if (initObj.hasOwnProperty('objectCounts')) {
        this.objectCounts = initObj.objectCounts
      }
      else {
        this.objectCounts = 0;
      }
      if (initObj.hasOwnProperty('centerX')) {
        this.centerX = initObj.centerX
      }
      else {
        this.centerX = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('centerY')) {
        this.centerY = initObj.centerY
      }
      else {
        this.centerY = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('centerZ')) {
        this.centerZ = initObj.centerZ
      }
      else {
        this.centerZ = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('lengthX')) {
        this.lengthX = initObj.lengthX
      }
      else {
        this.lengthX = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('lengthY')) {
        this.lengthY = initObj.lengthY
      }
      else {
        this.lengthY = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('lengthZ')) {
        this.lengthZ = initObj.lengthZ
      }
      else {
        this.lengthZ = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('minX')) {
        this.minX = initObj.minX
      }
      else {
        this.minX = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('minY')) {
        this.minY = initObj.minY
      }
      else {
        this.minY = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('minZ')) {
        this.minZ = initObj.minZ
      }
      else {
        this.minZ = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('maxX')) {
        this.maxX = initObj.maxX
      }
      else {
        this.maxX = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('maxY')) {
        this.maxY = initObj.maxY
      }
      else {
        this.maxY = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('maxZ')) {
        this.maxZ = initObj.maxZ
      }
      else {
        this.maxZ = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('pixelX')) {
        this.pixelX = initObj.pixelX
      }
      else {
        this.pixelX = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('pixelY')) {
        this.pixelY = initObj.pixelY
      }
      else {
        this.pixelY = new Array(100).fill(0);
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ObjectInfo
    // Serialize message field [objectCounts]
    bufferOffset = _serializer.int32(obj.objectCounts, buffer, bufferOffset);
    // Check that the constant length array field [centerX] has the right length
    if (obj.centerX.length !== 100) {
      throw new Error('Unable to serialize array field centerX - length must be 100')
    }
    // Serialize message field [centerX]
    bufferOffset = _arraySerializer.float64(obj.centerX, buffer, bufferOffset, 100);
    // Check that the constant length array field [centerY] has the right length
    if (obj.centerY.length !== 100) {
      throw new Error('Unable to serialize array field centerY - length must be 100')
    }
    // Serialize message field [centerY]
    bufferOffset = _arraySerializer.float64(obj.centerY, buffer, bufferOffset, 100);
    // Check that the constant length array field [centerZ] has the right length
    if (obj.centerZ.length !== 100) {
      throw new Error('Unable to serialize array field centerZ - length must be 100')
    }
    // Serialize message field [centerZ]
    bufferOffset = _arraySerializer.float64(obj.centerZ, buffer, bufferOffset, 100);
    // Check that the constant length array field [lengthX] has the right length
    if (obj.lengthX.length !== 100) {
      throw new Error('Unable to serialize array field lengthX - length must be 100')
    }
    // Serialize message field [lengthX]
    bufferOffset = _arraySerializer.float64(obj.lengthX, buffer, bufferOffset, 100);
    // Check that the constant length array field [lengthY] has the right length
    if (obj.lengthY.length !== 100) {
      throw new Error('Unable to serialize array field lengthY - length must be 100')
    }
    // Serialize message field [lengthY]
    bufferOffset = _arraySerializer.float64(obj.lengthY, buffer, bufferOffset, 100);
    // Check that the constant length array field [lengthZ] has the right length
    if (obj.lengthZ.length !== 100) {
      throw new Error('Unable to serialize array field lengthZ - length must be 100')
    }
    // Serialize message field [lengthZ]
    bufferOffset = _arraySerializer.float64(obj.lengthZ, buffer, bufferOffset, 100);
    // Check that the constant length array field [minX] has the right length
    if (obj.minX.length !== 100) {
      throw new Error('Unable to serialize array field minX - length must be 100')
    }
    // Serialize message field [minX]
    bufferOffset = _arraySerializer.float64(obj.minX, buffer, bufferOffset, 100);
    // Check that the constant length array field [minY] has the right length
    if (obj.minY.length !== 100) {
      throw new Error('Unable to serialize array field minY - length must be 100')
    }
    // Serialize message field [minY]
    bufferOffset = _arraySerializer.float64(obj.minY, buffer, bufferOffset, 100);
    // Check that the constant length array field [minZ] has the right length
    if (obj.minZ.length !== 100) {
      throw new Error('Unable to serialize array field minZ - length must be 100')
    }
    // Serialize message field [minZ]
    bufferOffset = _arraySerializer.float64(obj.minZ, buffer, bufferOffset, 100);
    // Check that the constant length array field [maxX] has the right length
    if (obj.maxX.length !== 100) {
      throw new Error('Unable to serialize array field maxX - length must be 100')
    }
    // Serialize message field [maxX]
    bufferOffset = _arraySerializer.float64(obj.maxX, buffer, bufferOffset, 100);
    // Check that the constant length array field [maxY] has the right length
    if (obj.maxY.length !== 100) {
      throw new Error('Unable to serialize array field maxY - length must be 100')
    }
    // Serialize message field [maxY]
    bufferOffset = _arraySerializer.float64(obj.maxY, buffer, bufferOffset, 100);
    // Check that the constant length array field [maxZ] has the right length
    if (obj.maxZ.length !== 100) {
      throw new Error('Unable to serialize array field maxZ - length must be 100')
    }
    // Serialize message field [maxZ]
    bufferOffset = _arraySerializer.float64(obj.maxZ, buffer, bufferOffset, 100);
    // Check that the constant length array field [pixelX] has the right length
    if (obj.pixelX.length !== 100) {
      throw new Error('Unable to serialize array field pixelX - length must be 100')
    }
    // Serialize message field [pixelX]
    bufferOffset = _arraySerializer.int64(obj.pixelX, buffer, bufferOffset, 100);
    // Check that the constant length array field [pixelY] has the right length
    if (obj.pixelY.length !== 100) {
      throw new Error('Unable to serialize array field pixelY - length must be 100')
    }
    // Serialize message field [pixelY]
    bufferOffset = _arraySerializer.int64(obj.pixelY, buffer, bufferOffset, 100);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ObjectInfo
    let len;
    let data = new ObjectInfo(null);
    // Deserialize message field [objectCounts]
    data.objectCounts = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [centerX]
    data.centerX = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [centerY]
    data.centerY = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [centerZ]
    data.centerZ = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [lengthX]
    data.lengthX = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [lengthY]
    data.lengthY = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [lengthZ]
    data.lengthZ = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [minX]
    data.minX = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [minY]
    data.minY = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [minZ]
    data.minZ = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [maxX]
    data.maxX = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [maxY]
    data.maxY = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [maxZ]
    data.maxZ = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [pixelX]
    data.pixelX = _arrayDeserializer.int64(buffer, bufferOffset, 100)
    // Deserialize message field [pixelY]
    data.pixelY = _arrayDeserializer.int64(buffer, bufferOffset, 100)
    return data;
  }

  static getMessageSize(object) {
    return 11204;
  }

  static datatype() {
    // Returns string type for a message object
    return 'lidar_interfaces/ObjectInfo';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '85c75bf95c45558608b5f8ca10538e49';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 objectCounts
    float64[100] centerX
    float64[100] centerY
    float64[100] centerZ
    float64[100] lengthX
    float64[100] lengthY
    float64[100] lengthZ
    float64[100] minX
    float64[100] minY
    float64[100] minZ
    float64[100] maxX
    float64[100] maxY
    float64[100] maxZ
    int64[100] pixelX
    int64[100] pixelY
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ObjectInfo(null);
    if (msg.objectCounts !== undefined) {
      resolved.objectCounts = msg.objectCounts;
    }
    else {
      resolved.objectCounts = 0
    }

    if (msg.centerX !== undefined) {
      resolved.centerX = msg.centerX;
    }
    else {
      resolved.centerX = new Array(100).fill(0)
    }

    if (msg.centerY !== undefined) {
      resolved.centerY = msg.centerY;
    }
    else {
      resolved.centerY = new Array(100).fill(0)
    }

    if (msg.centerZ !== undefined) {
      resolved.centerZ = msg.centerZ;
    }
    else {
      resolved.centerZ = new Array(100).fill(0)
    }

    if (msg.lengthX !== undefined) {
      resolved.lengthX = msg.lengthX;
    }
    else {
      resolved.lengthX = new Array(100).fill(0)
    }

    if (msg.lengthY !== undefined) {
      resolved.lengthY = msg.lengthY;
    }
    else {
      resolved.lengthY = new Array(100).fill(0)
    }

    if (msg.lengthZ !== undefined) {
      resolved.lengthZ = msg.lengthZ;
    }
    else {
      resolved.lengthZ = new Array(100).fill(0)
    }

    if (msg.minX !== undefined) {
      resolved.minX = msg.minX;
    }
    else {
      resolved.minX = new Array(100).fill(0)
    }

    if (msg.minY !== undefined) {
      resolved.minY = msg.minY;
    }
    else {
      resolved.minY = new Array(100).fill(0)
    }

    if (msg.minZ !== undefined) {
      resolved.minZ = msg.minZ;
    }
    else {
      resolved.minZ = new Array(100).fill(0)
    }

    if (msg.maxX !== undefined) {
      resolved.maxX = msg.maxX;
    }
    else {
      resolved.maxX = new Array(100).fill(0)
    }

    if (msg.maxY !== undefined) {
      resolved.maxY = msg.maxY;
    }
    else {
      resolved.maxY = new Array(100).fill(0)
    }

    if (msg.maxZ !== undefined) {
      resolved.maxZ = msg.maxZ;
    }
    else {
      resolved.maxZ = new Array(100).fill(0)
    }

    if (msg.pixelX !== undefined) {
      resolved.pixelX = msg.pixelX;
    }
    else {
      resolved.pixelX = new Array(100).fill(0)
    }

    if (msg.pixelY !== undefined) {
      resolved.pixelY = msg.pixelY;
    }
    else {
      resolved.pixelY = new Array(100).fill(0)
    }

    return resolved;
    }
};

module.exports = ObjectInfo;
