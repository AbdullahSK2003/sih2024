import { NextResponse } from 'next/server'
import { writeFile } from 'fs/promises'
import path from 'path'

export async function POST(request) {
  const data = await request.formData()
  const file = data.get('file')

  if (!file) {
    return NextResponse.json({ error: 'No file uploaded' }, { status: 400 })
  }

  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  const filename = `${Date.now()}-${file.name}`
  const filepath = path.join(process.cwd(), 'public', 'uploads', filename)
  await writeFile(filepath, buffer)

  const url = `/uploads/${filename}`
  return NextResponse.json({ url })
}