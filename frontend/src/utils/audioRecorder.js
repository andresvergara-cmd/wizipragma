/**
 * WAV Audio Recorder using Web Audio API
 * Records audio as raw PCM and encodes to WAV format
 * This produces clean WAV files that Amazon Transcribe handles perfectly,
 * unlike WebM/Opus which causes recognition issues with short clips.
 */

export class WavRecorder {
  constructor({ sampleRate = 16000, channelCount = 1 } = {}) {
    this.sampleRate = sampleRate
    this.channelCount = channelCount
    this.audioContext = null
    this.sourceNode = null
    this.processorNode = null
    this.stream = null
    this.chunks = []
    this.isRecording = false
  }

  async start() {
    this.chunks = []
    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        channelCount: this.channelCount,
        sampleRate: this.sampleRate,
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    })

    this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate: this.sampleRate
    })

    this.sourceNode = this.audioContext.createMediaStreamSource(this.stream)

    // Use ScriptProcessorNode to capture raw PCM samples
    // bufferSize 4096 is a good balance between latency and performance
    this.processorNode = this.audioContext.createScriptProcessor(4096, 1, 1)

    this.processorNode.onaudioprocess = (e) => {
      if (!this.isRecording) return
      const inputData = e.inputBuffer.getChannelData(0)
      // Copy the float32 samples
      this.chunks.push(new Float32Array(inputData))
    }

    this.sourceNode.connect(this.processorNode)
    this.processorNode.connect(this.audioContext.destination)
    this.isRecording = true
  }

  stop() {
    this.isRecording = false

    if (this.processorNode) {
      this.processorNode.disconnect()
      this.processorNode = null
    }
    if (this.sourceNode) {
      this.sourceNode.disconnect()
      this.sourceNode = null
    }
    if (this.stream) {
      this.stream.getTracks().forEach(t => t.stop())
      this.stream = null
    }

    const wavBlob = this._encodeWav()

    if (this.audioContext) {
      this.audioContext.close()
      this.audioContext = null
    }

    return wavBlob
  }

  _encodeWav() {
    // Merge all chunks into one Float32Array
    const totalLength = this.chunks.reduce((acc, c) => acc + c.length, 0)
    const merged = new Float32Array(totalLength)
    let offset = 0
    for (const chunk of this.chunks) {
      merged.set(chunk, offset)
      offset += chunk.length
    }

    // Convert float32 [-1,1] to int16 [-32768,32767]
    const pcm16 = new Int16Array(merged.length)
    for (let i = 0; i < merged.length; i++) {
      const s = Math.max(-1, Math.min(1, merged[i]))
      pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF
    }

    // Build WAV file
    const wavBuffer = new ArrayBuffer(44 + pcm16.length * 2)
    const view = new DataView(wavBuffer)

    // RIFF header
    this._writeString(view, 0, 'RIFF')
    view.setUint32(4, 36 + pcm16.length * 2, true)
    this._writeString(view, 8, 'WAVE')

    // fmt chunk
    this._writeString(view, 12, 'fmt ')
    view.setUint32(16, 16, true) // chunk size
    view.setUint16(20, 1, true)  // PCM format
    view.setUint16(22, this.channelCount, true)
    view.setUint32(24, this.sampleRate, true)
    view.setUint32(28, this.sampleRate * this.channelCount * 2, true) // byte rate
    view.setUint16(32, this.channelCount * 2, true) // block align
    view.setUint16(34, 16, true) // bits per sample

    // data chunk
    this._writeString(view, 36, 'data')
    view.setUint32(40, pcm16.length * 2, true)

    // Write PCM samples
    const pcmBytes = new Uint8Array(wavBuffer, 44)
    const pcmView = new Uint8Array(pcm16.buffer)
    pcmBytes.set(pcmView)

    return new Blob([wavBuffer], { type: 'audio/wav' })
  }

  _writeString(view, offset, str) {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i))
    }
  }
}
