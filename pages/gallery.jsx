/*
* Add the images in the public/images/gallery directory and all the images with valid/supported
* extensions (jpg/jpeg/png/gif) will be imported automatically and displayed into the ImageList.
*/

import fs from 'fs';
import path from 'path';

import Head from 'next/head';
import getConfig from 'next/config';

import { Box, Container, ImageList, ImageListItem, Typography } from '@mui/material';

const { publicRuntimeConfig } = getConfig();

export default function Gallery({ images }) {
    return (
        <>
            <Head>
                <title>Gallery | {publicRuntimeConfig.SCHOOL_NAME}</title>
            </Head>
            <Container sx={{ display : 'flex', flexDirection : 'columm', justifyContent : 'center', alignItems : 'center', padding : '8vh 0' }}>
                <Box sx={{
                    display         : 'flex',
                    flexDirection   : 'column',
                    alignItems      : 'center',
                    justifyContent  : 'center',
                    flexWrap        : 'wrap',
                    width           : { xs : '100%', sm : '90%' },
                    borderRadius    : '7.5px',
                    padding         : '50px 30px',
                    backgroundColor : 'background.paper'
                }}>
                    <Typography variant="h5">Gallery</Typography>
                    <Container sx={{ marginTop : '30px', maxWidth : { xs : '100%', sm : '95%', md : '90%', lg : '85%' } }}>
                        <ImageList variant="woven" cols={2} gap={8}>
                            {
                                images.map((val, index) => (
                                    <ImageListItem key={index} sx={{ position : 'relative' }}>
                                        {/* eslint-disable @next/next/no-img-element */}
                                        <img
                                            src={val}
                                            alt={val.split('/').slice(3).join()}
                                            layout="fill"
                                        />
                                        {/* eslint-enable */}
                                    </ImageListItem>
                                ))
                            }
                        </ImageList>
                    </Container>
                </Box>
            </Container>
        </>
    );
}

export function getStaticProps() {
    const GALLERY_PATH = 'images/gallery';
    const GALLERY_DIRECTORY = path.join(process.cwd(), 'public', GALLERY_PATH);

    let pattern = /^.*\.(jpg|jpeg|png|gif)$/i;
    let IMAGES = [];

    fs.readdirSync(GALLERY_DIRECTORY).forEach(file => {
        if (pattern.test(file)) {
            IMAGES.push(`/${GALLERY_PATH}/${file}`);
        }
    });

    return {
        props: {
            images: IMAGES
        },
    };
}
