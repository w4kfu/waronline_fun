unsigned int hash_filename(char *buffer, int seed, unsigned int size)
{
  int v5;
  int v6;
  unsigned int v7;
  int v8;
  int v9;
  int v10;
  int v11;
  int v12;
  int v13;
  int v14;
  unsigned int v17;
  int v19;
  int v20;
  int v21;
  int v23;
  int v24;
  unsigned int v25;

  v6 = 0x9E3779B9;
  v5 = 0x9E3779B9;
  if (size > 0xB)
  {
    v25 = size / 0xC;
    do
    {
      v17 = (unsigned __int8)buffer[8]
          + (((unsigned __int8)buffer[9] + (((unsigned __int8)buffer[10] + ((unsigned __int8)buffer[11] << 8)) << 8)) << 8)
          + seed;
      v6 = v6
          + (unsigned __int8)buffer[4]
          + (((unsigned __int8)buffer[5] + (((unsigned __int8)buffer[6] + ((unsigned __int8)buffer[7] << 8)) << 8)) << 8);
      v19 = (v17 >> 13) ^ ((unsigned __int8)*buffer
                         + (((unsigned __int8)buffer[1] + (((unsigned __int8)buffer[2] + ((unsigned __int8)buffer[3] << 8)) << 8)) << 8)
                         + v5
                         - v17
                         - v6);
      v20 = (v6 - v17 - v19) ^ (v19 << 8);
      v21 = ((unsigned int)v20 >> 13) ^ (v17 - v20 - v19);
      buffer += 12;
      v23 = ((((unsigned int)v21 >> 12) ^ (v19 - v21 - v20)) << 16) ^ (v20 - v21 - (((unsigned int)v21 >> 12) ^ (v19 - v21 - v20)));
      v24 = ((unsigned int)v23 >> 5) ^ (v21 - v23 - (((unsigned int)v21 >> 12) ^ (v19 - v21 - v20)));
      v5 = ((unsigned int)v24 >> 3) ^ ((((unsigned int)v21 >> 12) ^ (v19 - v21 - v20)) - v24 - v23);
      v6 = (v5 << 10) ^ (v23 - v24 - v5);
      seed = ((unsigned int)v6 >> 15) ^ (v24 - v6 - v5);
      --v25;
    }
    while (v25);
    buffer += 12 * size / 0xC;
	v7 = size + seed;
    size = size % 0xC;
  }
  else
	v7 = size + seed;
  switch (size)
  {
    case 0xB:
      v7 += (unsigned __int8)buffer[10] << 24;
    case 0xA:
      v7 += (unsigned __int8)buffer[9] << 16;
    case 0x9:
      v7 += (unsigned __int8)buffer[8] << 8;
    case 0x8:
      v6 += (unsigned __int8)buffer[7] << 24;
    case 0x7:
      v6 += (unsigned __int8)buffer[6] << 16;
    case 0x6:
      v6 += (unsigned __int8)buffer[5] << 8;
    case 0x5:
      v6 += (unsigned __int8)buffer[4];
    case 0x4:
      v5 += (unsigned __int8)buffer[3] << 24;
    case 0x3:
      v5 += (unsigned __int8)buffer[2] << 16;
    case 0x2:
      v5 += (unsigned __int8)buffer[1] << 8;
    case 0x1:
      v5 += (unsigned __int8)*buffer;
    default:
      break;
  }
  v8 = (v7 >> 13) ^ (v5 - v7 - v6);
  v9 = (v6 - v7 - v8) ^ (v8 << 8);
  v10 = (v7 - v9 - v8) ^ ((unsigned int)v9 >> 13);
  v11 = ((unsigned int)v10 >> 12) ^ (v8 - v10 - v9);
  v12 = (v11 << 16) ^ (v9 - v10 - v11);
  v13 = ((unsigned int)v12 >> 5) ^ (v10 - v12 - v11);
  v14 = ((unsigned int)v13 >> 3) ^ (v11 - v13 - v12);
  return (((v14 << 10) ^ (unsigned int)(v12 - v13 - v14)) >> 15) ^ (v13 - ((v14 << 10) ^ (v12 - v13 - v14)) - v14);
}